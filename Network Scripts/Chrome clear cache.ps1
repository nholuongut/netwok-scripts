$chromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$numThreads = 2

function Clear-Chrome-Cache {
    try {
        Stop-Process -Name "chrome" -Force

        $cacheClearCommand = @(
            $chromePath,
            "--user-data-dir=TempProfile",
            "--disk-cache-size=1",
            "--media-cache-size=1",
            "--disable-application-cache"
        )

        Start-Process -FilePath $cacheClearCommand[0] -ArgumentList $cacheClearCommand[1..$cacheClearCommand.Length] -Wait

        $tempProfileDir = Join-Path $env:USERPROFILE "TempProfile"
        if (Test-Path $tempProfileDir) {
            Remove-Item $tempProfileDir -Force -Recurse
        }

        Write-Host "Chrome cache has been cleared."
    }
    catch {
        Write-Host "An error occurred: $_"
    }
}

$threads = @()

for ($i = 0; $i -lt $numThreads; $i++) {
    $thread = [System.Threading.Thread]::new({ Clear-Chrome-Cache })
    $threads += $thread
    $thread.Start()
}

$threads | ForEach-Object { $_.Join() }