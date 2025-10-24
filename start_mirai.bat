@echo off
REM ╔══════════════════════════════════════════════════════════════════════╗
REM ║                    MIRAI - Единый Автономный Агент                  ║
REM ║                          Быстрый запуск                             ║
REM ╚══════════════════════════════════════════════════════════════════════╝

echo.
echo ╔══════════════════════════════════════════════════════════════════════╗
echo ║                    MIRAI - Единый Автономный Агент                  ║
echo ╚══════════════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0mirai-agent"

REM Проверка Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден! Установите Python 3.10+
    pause
    exit /b 1
)

REM Проверка зависимостей
if not exist "venv\" (
    echo 📦 Создание виртуального окружения...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo 📦 Установка зависимостей...
    pip install --upgrade pip
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
    echo 📦 Проверка зависимостей...
    pip install --upgrade pip --quiet
    pip install -r requirements.txt --quiet
)

REM Проверка API ключей
if not exist "configs\api_keys.json" (
    echo.
    echo ⚠️  ВНИМАНИЕ: Не найден файл configs/api_keys.json
    echo.
    echo Создайте файл configs/api_keys.json с содержимым:
    echo {
    echo   "openai": "sk-your-api-key-here",
    echo   "github_token": "ghp_your_token_here"
    echo }
    echo.
    pause
    exit /b 1
)

REM Запуск MIRAI
echo.
echo 🚀 Запуск MIRAI...
echo.
python unified_mirai.py

pause
