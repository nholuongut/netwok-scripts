$chromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$numThreads = 2

# Function to clear Chrome cache for a given user data directory
function Clear-Chrome-Cache {
    param (
        [string]$userDataDir,
        [string]$chromePath
    )
    try {
        # Stop Chrome processes
        Stop-Process -Name "chrome" -Force -ErrorAction SilentlyContinue

        $cacheClearCommand = @(
            $chromePath,
            "--user-data-dir=$userDataDir",
            "--disk-cache-size=1",
            "--media-cache-size=1",
            "--disable-application-cache"
        )

        # Start Chrome to clear cache
        Start-Process -FilePath $cacheClearCommand[0] -ArgumentList $cacheClearCommand[1..$cacheClearCommand.Length] -Wait

        # Remove the temporary profile directory
        if (Test-Path $userDataDir) {
            Remove-Item $userDataDir -Force -Recurse
        }

        Write-Host "Chrome cache has been cleared for user data directory: $userDataDir"
    }
    catch {
        Write-Host "An error occurred: $_"
    }
}

# Function to start multiple threads
function Start-Multiple-Threads {
    param (
        [int]$numThreads,
        [scriptblock]$scriptBlock
    )
    $threads = @()

    for ($i = 0; $i -lt $numThreads; $i++) {
        $thread = [System.Threading.Thread]::new($scriptBlock)
        $threads += $thread
        $thread.Start()
    }

    $threads | ForEach-Object { $_.Join() }
}

# Define a unique user data directory for each thread and clear Chrome cache in parallel
for ($i = 0; $i -lt $numThreads; $i++) {
    $userDataDir = Join-Path $env:USERPROFILE "TempProfile$i"
    
    # Use the Start-Multiple-Threads function to run multiple threads
    Start-Multiple-Threads -numThreads $numThreads -scriptBlock {
        param (
            [string]$userDataDir,
            [string]$chromePath
        )
        Clear-Chrome-Cache -userDataDir $userDataDir -chromePath $chromePath
    } -userDataDir $userDataDir -chromePath $chromePath
}

# Notify when all threads have completed
Write-Host "All threads have completed."