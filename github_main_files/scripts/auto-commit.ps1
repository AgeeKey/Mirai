# 🔥 EXTREME Copilot Auto Accept Configuration
# PowerShell скрипт для автоматических коммитов
# ПРЕДУПРЕЖДЕНИЕ: Используйте только в экспериментальных проектах!

param(
    [string]$ConfigPath = ".\scripts\auto-commit-config.json",
    [switch]$DryRun = $false,
    [switch]$Verbose = $false
)

# Загрузка конфигурации
if (-not (Test-Path $ConfigPath)) {
    Write-Error "❌ Конфигурационный файл не найден: $ConfigPath"
    exit 1
}

$config = Get-Content $ConfigPath | ConvertFrom-Json
Write-Host "🔧 Загружена конфигурация из: $ConfigPath" -ForegroundColor Green

# Функция логирования
function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $color = switch ($Level) {
        "INFO" { "White" }
        "WARN" { "Yellow" }
        "ERROR" { "Red" }
        "SUCCESS" { "Green" }
        default { "White" }
    }
    Write-Host "[$timestamp] [$Level] $Message" -ForegroundColor $color
}

# Проверка Git репозитория
if (-not (Test-Path ".git")) {
    Write-Log "❌ Не найден Git репозиторий в текущей директории" "ERROR"
    exit 1
}

Write-Log "🚀 Запуск ЭКСТРЕМАЛЬНОГО авто-коммита..." "INFO"
Write-Log "⏱️ Интервал: $($config.intervalMinutes) минут" "INFO"
Write-Log "📁 Максимальный размер файла: $($config.maxFileSizeKB) KB" "INFO"

# Функция выполнения авто-коммита
function Invoke-AutoCommit {
    try {
        # Проверка изменений
        $status = git status --porcelain
        if (-not $status) {
            if ($Verbose) {
                Write-Log "✅ Нет изменений для коммита" "INFO"
            }
            return
        }

        Write-Log "📝 Обнаружены изменения:" "INFO"
        if ($Verbose) {
            $status | ForEach-Object { Write-Log "  $_" "INFO" }
        }

        # Фильтрация больших файлов
        $largeFiles = @()
        git diff --cached --name-only 2>$null | ForEach-Object {
            $file = $_
            if (Test-Path $file) {
                $sizeKB = (Get-Item $file).Length / 1024
                if ($sizeKB -gt $config.maxFileSizeKB) {
                    $largeFiles += $file
                }
            }
        }

        if ($largeFiles.Count -gt 0) {
            Write-Log "⚠️ Пропуск больших файлов: $($largeFiles -join ', ')" "WARN"
            $largeFiles | ForEach-Object { git reset HEAD $_ 2>$null }
        }

        # Добавление изменений
        if (-not $DryRun) {
            git add .
            
            # Создание commit message
            $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
            $commitMsg = "$($config.commitPrefix) $timestamp"
            
            if ($config.includeFileCount) {
                $fileCount = (git diff --cached --name-only | Measure-Object).Count
                $commitMsg += " ($fileCount files)"
            }

            # Выполнение коммита
            git commit -m $commitMsg

            if ($LASTEXITCODE -eq 0) {
                Write-Log "✅ Коммит выполнен: $commitMsg" "SUCCESS"
                
                # Автопуш (если включен)
                if ($config.autoPush) {
                    Write-Log "📤 Выполняется автопуш..." "INFO"
                    git push origin HEAD
                    if ($LASTEXITCODE -eq 0) {
                        Write-Log "✅ Пуш выполнен успешно" "SUCCESS"
                    } else {
                        Write-Log "❌ Ошибка при пуше" "ERROR"
                    }
                }
            } else {
                Write-Log "❌ Ошибка при создании коммита" "ERROR"
            }
        } else {
            Write-Log "🔍 DRY RUN: Коммит не выполнен" "WARN"
        }

    } catch {
        Write-Log "❌ Ошибка при выполнении авто-коммита: $($_.Exception.Message)" "ERROR"
    }
}

# Основной цикл
if ($config.runOnce) {
    Write-Log "🔄 Выполнение одиночного коммита..." "INFO"
    Invoke-AutoCommit
} else {
    Write-Log "🔄 Запуск циклического режима..." "INFO"
    Write-Log "⚠️ Для остановки нажмите Ctrl+C" "WARN"
    
    $intervalMs = $config.intervalMinutes * 60 * 1000
    
    while ($true) {
        Invoke-AutoCommit
        
        if ($Verbose) {
            Write-Log "⏳ Ожидание $($config.intervalMinutes) минут до следующего цикла..." "INFO"
        }
        
        Start-Sleep -Milliseconds $intervalMs
    }
}

Write-Log "🏁 Скрипт завершен" "INFO"