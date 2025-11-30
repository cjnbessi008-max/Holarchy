# ============================================================
# 🔧 Holarchy Git 동기화 스케줄러 설치
# 1시간마다 변경 감지 + 알림
# ============================================================

Write-Host "============================================================"
Write-Host "🔧 Holarchy Git 동기화 스케줄러 설치"
Write-Host "============================================================"
Write-Host ""

$scriptPath = "C:\1 Project\Holarchy\git_sync_notify.ps1"
$taskName = "Holarchy Git Sync Notify"

# 기존 작업 삭제 (있으면)
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "⚠️ 기존 작업 발견 - 삭제 중..."
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# 새 작업 등록
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" `
    -Argument "-ExecutionPolicy Bypass -WindowStyle Hidden -File `"$scriptPath`""

$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) `
    -RepetitionInterval (New-TimeSpan -Hours 1) `
    -RepetitionDuration (New-TimeSpan -Days 365)

$settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -DontStopOnIdleEnd `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries

$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive

Register-ScheduledTask `
    -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Principal $principal `
    -Description "1시간마다 Holarchy 변경사항 확인 후 Push 알림"

Write-Host ""
Write-Host "✅ 설치 완료!"
Write-Host ""
Write-Host "📋 설정 정보:"
Write-Host "   • 작업 이름: $taskName"
Write-Host "   • 실행 간격: 1시간"
Write-Host "   • 스크립트: $scriptPath"
Write-Host ""
Write-Host "💡 사용 방법:"
Write-Host "   • 변경사항 있으면 팝업 알림 표시"
Write-Host "   • '예' 선택 시 커밋 메시지 입력 후 Push"
Write-Host "   • '아니오' 선택 시 무시"
Write-Host ""
Write-Host "🔧 관리 명령어:"
Write-Host "   • 즉시 실행: Start-ScheduledTask -TaskName '$taskName'"
Write-Host "   • 중지: Disable-ScheduledTask -TaskName '$taskName'"
Write-Host "   • 삭제: Unregister-ScheduledTask -TaskName '$taskName'"
Write-Host ""
Write-Host "============================================================"

