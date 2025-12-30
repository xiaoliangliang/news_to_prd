# NewstoPRD 冒烟测试脚本
# 启动系统并验证基本功能

param(
    [int]$WaitSeconds = 90,  # 等待时间（秒）
    [switch]$SkipStart       # 跳过启动（假设系统已运行）
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$DemoDir = Split-Path -Parent $ScriptDir

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  NewstoPRD - 冒烟测试" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 如果需要，启动系统
if (-not $SkipStart) {
    Write-Host "启动系统（单次运行模式）..." -ForegroundColor Yellow
    
    # 在后台启动 run_all.ps1
    $startJob = Start-Job -ScriptBlock {
        param($scriptPath)
        & $scriptPath -RunOnce
    } -ArgumentList "$ScriptDir\run_all.ps1"
    
    Write-Host "等待系统启动..." -ForegroundColor Yellow
    Start-Sleep -Seconds 10
}

Write-Host ""
Write-Host "等待 $WaitSeconds 秒让流水线完成..." -ForegroundColor Yellow
Write-Host ""

# 显示进度条
$startTime = Get-Date
for ($i = 0; $i -lt $WaitSeconds; $i += 5) {
    $elapsed = (Get-Date) - $startTime
    $progress = [math]::Round(($i / $WaitSeconds) * 100)
    Write-Progress -Activity "等待流水线完成" -Status "$progress% 完成" -PercentComplete $progress
    Start-Sleep -Seconds 5
}
Write-Progress -Activity "等待流水线完成" -Completed

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  验证结果" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$passed = $true

# 检查 1: Network 是否运行
Write-Host "[检查 1] Network 运行状态..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8800" -TimeoutSec 5 -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        Write-Host "  ✓ Network 正在运行 (HTTP:8800)" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Network 响应异常" -ForegroundColor Red
        $passed = $false
    }
} catch {
    Write-Host "  ✗ Network 未响应" -ForegroundColor Red
    $passed = $false
}

# 检查 2: 日志文件存在
Write-Host "[检查 2] 日志文件..." -ForegroundColor Yellow
$logFiles = @(
    "logs/llm/router.jsonl",
    "logs/llm/web-searcher.jsonl",
    "logs/llm/analyst.jsonl"
)

foreach ($logFile in $logFiles) {
    $fullPath = Join-Path $DemoDir $logFile
    if (Test-Path $fullPath) {
        $size = (Get-Item $fullPath).Length
        Write-Host "  ✓ $logFile 存在 ($size bytes)" -ForegroundColor Green
    } else {
        Write-Host "  ○ $logFile 不存在（可能尚未触发）" -ForegroundColor Yellow
    }
}

# 检查 3: 查找调研报告输出
Write-Host "[检查 3] 调研报告输出..." -ForegroundColor Yellow
$routerLog = Join-Path $DemoDir "logs/llm/router.jsonl"
if (Test-Path $routerLog) {
    $content = Get-Content $routerLog -Raw
    if ($content -match "调研报告|Research Report|市场趋势|竞品分析") {
        Write-Host "  ✓ 发现调研报告输出" -ForegroundColor Green
    } else {
        Write-Host "  ○ 未发现调研报告（可能流水线尚未完成）" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ○ Router 日志不存在" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

if ($passed) {
    Write-Host "  冒烟测试通过!" -ForegroundColor Green
} else {
    Write-Host "  冒烟测试有警告，请检查上述输出" -ForegroundColor Yellow
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "提示: 访问 http://localhost:8800 查看 Studio 界面" -ForegroundColor Cyan
Write-Host ""

# 清理
if (-not $SkipStart -and $startJob) {
    Write-Host "停止后台进程..." -ForegroundColor Yellow
    Stop-Job $startJob -ErrorAction SilentlyContinue
    Remove-Job $startJob -ErrorAction SilentlyContinue
}
