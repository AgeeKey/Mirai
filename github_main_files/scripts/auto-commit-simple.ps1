# EXTREME Auto-Commit Script
# PowerShell script for automatic commits
# WARNING: Use only in experimental projects!

param(
    [switch]$DryRun = $false,
    [switch]$Verbose = $false
)

# Load configuration
$configPath = ".\scripts\auto-commit-config.json"
if (-not (Test-Path $configPath)) {
    Write-Error "Configuration file not found: $configPath"
    exit 1
}

$config = Get-Content $configPath | ConvertFrom-Json
Write-Host "Configuration loaded from: $configPath" -ForegroundColor Green

# Logging function
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

# Check Git repository
if (-not (Test-Path ".git")) {
    Write-Log "No Git repository found in current directory" "ERROR"
    exit 1
}

Write-Log "Starting EXTREME auto-commit..." "INFO"
Write-Log "Interval: $($config.intervalMinutes) minutes" "INFO"
Write-Log "Max file size: $($config.maxFileSizeKB) KB" "INFO"

# Auto-commit function
function Invoke-AutoCommit {
    try {
        # Check for changes
        $status = git status --porcelain
        if (-not $status) {
            if ($Verbose) {
                Write-Log "No changes to commit" "INFO"
            }
            return
        }

        Write-Log "Changes detected:" "INFO"
        if ($Verbose) {
            $status | ForEach-Object { Write-Log "  $_" "INFO" }
        }

        # Add changes
        if (-not $DryRun) {
            git add .
            
            # Create commit message
            $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
            $commitMsg = "$($config.commitPrefix) $timestamp"
            
            if ($config.includeFileCount) {
                $fileCount = (git diff --cached --name-only | Measure-Object).Count
                $commitMsg += " ($fileCount files)"
            }

            # Execute commit
            git commit -m $commitMsg

            if ($LASTEXITCODE -eq 0) {
                Write-Log "Commit successful: $commitMsg" "SUCCESS"
                
                # Auto-push if enabled
                if ($config.autoPush) {
                    Write-Log "Executing auto-push..." "INFO"
                    git push origin HEAD
                    if ($LASTEXITCODE -eq 0) {
                        Write-Log "Push successful" "SUCCESS"
                    } else {
                        Write-Log "Push failed" "ERROR"
                    }
                }
            } else {
                Write-Log "Commit failed" "ERROR"
            }
        } else {
            Write-Log "DRY RUN: Commit not executed" "WARN"
        }

    } catch {
        Write-Log "Error during auto-commit: $($_.Exception.Message)" "ERROR"
    }
}

# Main loop
if ($config.runOnce) {
    Write-Log "Executing single commit..." "INFO"
    Invoke-AutoCommit
} else {
    Write-Log "Starting cyclic mode..." "INFO"
    Write-Log "Press Ctrl+C to stop" "WARN"
    
    $intervalMs = $config.intervalMinutes * 60 * 1000
    
    while ($true) {
        Invoke-AutoCommit
        
        if ($Verbose) {
            Write-Log "Waiting $($config.intervalMinutes) minutes until next cycle..." "INFO"
        }
        
        Start-Sleep -Milliseconds $intervalMs
    }
}

Write-Log "Script completed" "INFO"