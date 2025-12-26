@echo off
REM Quick Start Script for MoneyPrinter Automation (Windows)

echo MoneyPrinter Automation Setup
echo =================================
echo.

REM Check if automation_config.yaml exists
if exist automation_config.yaml (
    echo [OK] Configuration file exists: automation_config.yaml
) else (
    echo [!] No automation_config.yaml found
    echo     Copying from example file...
    copy automation_config.example.yaml automation_config.yaml
    echo [OK] Created automation_config.yaml
    echo.
    echo Please edit automation_config.yaml to configure your automation settings
    echo Key settings to review:
    echo   - video_topics: Add your video topics
    echo   - automate_youtube_upload: Enable when you've set up OAuth
    echo   - generation_interval_hours: How often to generate videos
    echo.
)

REM Check if PyYAML is installed
echo.
echo Checking dependencies...
python -c "import yaml" 2>nul
if %errorlevel% equ 0 (
    echo [OK] PyYAML is installed
) else (
    echo [!] PyYAML is not installed
    echo     Installing PyYAML...
    pip install PyYAML==6.0.1
    if %errorlevel% equ 0 (
        echo [OK] PyYAML installed successfully
    ) else (
        echo [ERROR] Failed to install PyYAML
        echo Please run: pip install PyYAML==6.0.1
        pause
        exit /b 1
    )
)

REM Check if backend is running
echo.
echo Checking backend connection...
curl -s http://localhost:8080/api/cancel >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Backend is running
) else (
    echo [!] Backend is not running
    echo.
    echo     The MoneyPrinter backend must be running for automation to work.
    echo     Start it with:
    echo     cd Backend
    echo     python main.py
    echo.
    pause
)

echo.
echo =================================
echo Setup complete!
echo.
echo Usage:
echo   python automation.py              # Run once
echo   python automation.py --daemon     # Run continuously
echo.
echo For more information, see AUTOMATION.md
echo.
pause
