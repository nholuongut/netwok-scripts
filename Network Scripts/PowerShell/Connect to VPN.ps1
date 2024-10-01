param (
    $timeout = 60
)

# Function to get a list of available VPN connections
function Get-VPNConnections {
    Get-VpnConnection | Select-Object -Property Name, ServerAddress
}

# Function to display a list of VPN connections with numbers and spacing
function Display-VPNConnections($connections) {
    Write-Output "Available VPN Connections:"
    $connections | ForEach-Object {
        $index = $_.PSObject.Properties['Index'].Value
        $formattedIndex = "{0,-3}" -f $index  # Add spacing for alignment
        Write-Output "$formattedIndex. $($_.Name) - $($_.ServerAddress)"
    }
}

# Function to connect to the selected VPN connection (if available)
function Connect-To-VPN($connection) {
    if ($connection) {
        Write-Output "Connecting to $($connection.Name)..."
        $connectResult = Start-Job -ScriptBlock {
            param ($connectionName)
            Connect-VpnS2SInterface -Name $connectionName
        } -ArgumentList $connection.Name

        $jobCompleted = $false
        $jobOutput = $null
        do {
            $jobOutput = Receive-Job $connectResult -ErrorAction SilentlyContinue
            if ($jobOutput -match "Connected") {
                $jobCompleted = $true
                Write-Output "Connected to $($connection.Name)."
            } elseif ($jobOutput -match "Failed") {
                $jobCompleted = $true
                Write-Output "Connection to $($connection.Name) failed."
            } else {
                Start-Sleep -Seconds 1
            }
        } while (-not $jobCompleted -and $timeout -gt 0)

        Remove-Job $connectResult  # Clean up the job
    } else {
        Write-Output "Selected VPN connection not found."
    }
}

# Main script logic
$vpnConnections = Get-VPNConnections | ForEach-Object {
    [PSCustomObject]@{
        Index = $_.PSObject.Properties['Name'].Value
        Name = $_.Name
        ServerAddress = $_.ServerAddress
    }
}
Display-VPNConnections $vpnConnections

do {
    $selectedIndex = Read-Host "Enter the number of the VPN connection you want to connect to"

    if (-not ([int]::TryParse($selectedIndex, [ref]$null) -and $selectedIndex -ge 1 -and $selectedIndex -le $vpnConnections.Count)) {
        Write-Output "Invalid selection. Please enter a valid number."
    }
} while (-not ([int]::TryParse($selectedIndex, [ref]$null) -and $selectedIndex -ge 1 -and $selectedIndex -le $vpnConnections.Count))

$selectedConnection = $vpnConnections | Where-Object { $_.Index -eq [int]$selectedIndex }
Connect-To-VPN $selectedConnection