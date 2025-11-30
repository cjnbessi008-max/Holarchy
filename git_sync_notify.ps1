# ============================================================
# 🔔 Holarchy Git 동기화 알림 스크립트
# 1시간마다 변경사항 확인 후 Push 여부 선택
# + 🏥 Health Check 통합
# ============================================================

$repoPath = "C:\1 Project\Holarchy"
$holonsPath = "C:\1 Project\Holarchy\0 Docs\holons"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# 작업 디렉토리로 이동
Set-Location $repoPath

# Git 상태 확인
$status = git status --porcelain
$changedFiles = ($status | Measure-Object -Line).Lines

if ($changedFiles -gt 0) {
    # 변경된 파일 목록 생성
    $fileList = $status | Select-Object -First 10
    $fileListText = $fileList -join "`n"
    
    if ($changedFiles -gt 10) {
        $fileListText += "`n... 외 $($changedFiles - 10)개 파일"
    }
    
    # 🏥 Health Check 실행
    Set-Location $holonsPath
    $healthOutput = python _health_check.py check 2>&1 | Out-String
    
    # 건강도 추출 (정규식)
    $healthMatch = [regex]::Match($healthOutput, '전체 건강도: (\d+)%')
    if ($healthMatch.Success) {
        $healthScore = [int]$healthMatch.Groups[1].Value
    } else {
        $healthScore = -1
    }
    
    # 건강 상태 아이콘
    if ($healthScore -ge 80) {
        $healthIcon = "🟢"
        $healthStatus = "양호"
    } elseif ($healthScore -ge 60) {
        $healthIcon = "🟡"
        $healthStatus = "주의"
    } elseif ($healthScore -ge 0) {
        $healthIcon = "🔴"
        $healthStatus = "위험"
    } else {
        $healthIcon = "❓"
        $healthStatus = "확인 불가"
    }
    
    Set-Location $repoPath
    
    # 팝업 메시지 박스 표시
    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -AssemblyName System.Drawing
    
    $message = @"
📂 Holarchy 프로젝트에 변경사항이 있습니다.

📊 변경된 파일: $changedFiles 개
$healthIcon 시스템 건강도: $healthScore% ($healthStatus)

📋 변경 목록:
$fileListText

GitHub에 Push 하시겠습니까?
"@
    
    # 건강도가 80% 미만이면 경고 아이콘 사용
    $iconType = [System.Windows.Forms.MessageBoxIcon]::Question
    if ($healthScore -lt 80 -and $healthScore -ge 0) {
        $iconType = [System.Windows.Forms.MessageBoxIcon]::Warning
    }
    
    $result = [System.Windows.Forms.MessageBox]::Show(
        $message,
        "🔔 Holarchy Git 동기화 - $timestamp",
        [System.Windows.Forms.MessageBoxButtons]::YesNo,
        $iconType
    )
    
    if ($result -eq [System.Windows.Forms.DialogResult]::Yes) {
        # Push 실행
        try {
            git add -A
            $commitMsg = Read-Host "커밋 메시지 입력 (Enter = 자동 메시지)"
            
            if ([string]::IsNullOrWhiteSpace($commitMsg)) {
                $commitMsg = "Sync: $timestamp - $changedFiles files changed"
            }
            
            git commit -m $commitMsg
            git push origin main
            
            [System.Windows.Forms.MessageBox]::Show(
                "✅ Push 완료!`n`n커밋: $commitMsg",
                "Holarchy Git 동기화",
                [System.Windows.Forms.MessageBoxButtons]::OK,
                [System.Windows.Forms.MessageBoxIcon]::Information
            )
        }
        catch {
            [System.Windows.Forms.MessageBox]::Show(
                "❌ Push 실패!`n`n오류: $_",
                "Holarchy Git 동기화",
                [System.Windows.Forms.MessageBoxButtons]::OK,
                [System.Windows.Forms.MessageBoxIcon]::Error
            )
        }
    }
    else {
        # 사용자가 "아니오" 선택
        Write-Host "ℹ️ Push 취소됨: $timestamp"
    }
}
else {
    # 변경사항 없음 - 조용히 종료 (알림 없음)
    Write-Host "ℹ️ 변경사항 없음: $timestamp"
}
