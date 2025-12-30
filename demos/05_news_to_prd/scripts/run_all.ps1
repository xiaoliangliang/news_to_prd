# NewstoPRD - One-click startup script
# Starts network and all agents

param(
    [switch]$RunOnce,
    [int]$Interval = 300
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$DemoDir = Split-Path -Parent $ScriptDir

Write-Host "========================================"
Write-Host "  NewstoPRD - Starting..."
Write-Host "========================================"
Write-Host "Demo Dir: $DemoDir"
Write-Host "Run Once: $RunOnce"
Write-Host "Interval: $Interval seconds"
Write-Host ""

Set-Location $DemoDir

Write-Host "[1/7] Starting Network..."
$networkJob = Start-Job -ScriptBlock {
    param($d)
    Set-Location $d
    openagents network start network.yaml
} -ArgumentList $DemoDir

Start-Sleep -Seconds 5

Write-Host "[2/7] Starting Router..."
$routerJob = Start-Job -ScriptBlock {
    param($d)
    Set-Location $d
    openagents agent start agents/router.yaml
} -ArgumentList $DemoDir

Start-Sleep -Seconds 2

Write-Host "[3/7] Starting Web Searcher..."
$webSearcherJob = Start-Job -ScriptBlock {
    param($d)
    Set-Location $d
    openagents agent start agents/web_searcher.yaml
} -ArgumentList $DemoDir

Start-Sleep -Seconds 2

Write-Host "[4/7] Starting Analyst..."
$analystJob = Start-Job -ScriptBlock {
    param($d)
    Set-Location $d
    openagents agent start agents/analyst.yaml
} -ArgumentList $DemoDir

Start-Sleep -Seconds 2

Write-Host "[5/7] Starting Product Insight..."
$productInsightJob = Start-Job -ScriptBlock {
    param($d)
    Set-Location $d
    openagents agent start agents/product_insight.yaml
} -ArgumentList $DemoDir

Start-Sleep -Seconds 2

Write-Host "[6/7] Starting PRD Expert..."
$prdExpertJob = Start-Job -ScriptBlock {
    param($d)
    Set-Location $d
    openagents agent start agents/prd_expert.yaml
} -ArgumentList $DemoDir

Start-Sleep -Seconds 2

Write-Host "[7/7] Starting News Hunter..."
if ($RunOnce) {
    $newsHunterJob = Start-Job -ScriptBlock {
        param($d, $i)
        Set-Location $d
        python agents/news_hunter.py --host localhost --port 8800 --interval $i --run-once
    } -ArgumentList $DemoDir, $Interval
} else {
    $newsHunterJob = Start-Job -ScriptBlock {
        param($d, $i)
        Set-Location $d
        python agents/news_hunter.py --host localhost --port 8800 --interval $i
    } -ArgumentList $DemoDir, $Interval
}

Write-Host ""
Write-Host "========================================"
Write-Host "  All components started!"
Write-Host "========================================"
Write-Host ""
Write-Host "Studio URL: http://localhost:8800"
Write-Host ""
Write-Host "Press Ctrl+C to stop all components"
Write-Host ""

try {
    while ($true) {
        Start-Sleep -Seconds 10
    }
}
finally {
    Write-Host "Stopping all components..."
    Get-Job | Stop-Job -ErrorAction SilentlyContinue
    Get-Job | Remove-Job -ErrorAction SilentlyContinue
    Write-Host "All components stopped."
}
