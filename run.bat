@echo off
chcp 65001 >nul
title Image Processing Pipeline

echo ========================================
echo Image Processing Pipeline
echo Order: Background Removal -^> Element Extraction -^> Color Analysis
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not detected, please install Python 3.8+
    echo Download: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo [INFO] Virtual environment detected, activating...
    call venv\Scripts\activate.bat
    if errorlevel 1 (
        echo [WARNING] Virtual environment activation failed, using system Python
    ) else (
        echo [SUCCESS] Virtual environment activated
    )
) else (
    echo [INFO] No virtual environment detected, using system Python
)

echo.
echo ========================================
echo Step 1: Background Removal
echo ========================================
echo.

echo [INFO] Running rmbg.py...
python rmbg.py
if errorlevel 1 (
    echo [ERROR] Background removal failed
    pause
    exit /b 1
) else (
    echo [SUCCESS] Background removal completed
)

echo.
echo ========================================
echo Step 2: Element Extraction
echo ========================================
echo.

echo [INFO] Running grid_split_elements.py...
python grid_split_elements.py
if errorlevel 1 (
    echo [ERROR] Element extraction failed
    pause
    exit /b 1
) else (
    echo [SUCCESS] Element extraction completed
)

echo.
echo ========================================
echo Step 3: Color Analysis
echo ========================================
echo.

echo [INFO] Running color_analyzer.py...
python color_analyzer.py --summary
if errorlevel 1 (
    echo [ERROR] Color analysis failed
    pause
    exit /b 1
) else (
    echo [SUCCESS] Color analysis completed
)

echo.
echo ========================================
echo Pipeline Execution Completed
echo ========================================
echo.
echo [SUCCESS] All steps completed successfully!
echo.
echo Check individual script documentation for output files
echo.
pause