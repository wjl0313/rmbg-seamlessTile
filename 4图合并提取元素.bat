@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

:: 激活虚拟环境
call .\venv\Scripts\activate

:: 设置默认值
set "OUTPUT_DIR=merged_output"
set "MIN_AREA=100"

echo ========================================
echo    四方连续图片合并元素提取工具
echo ========================================
echo.
echo 功能说明:
echo 1. 将一张四方连续图片复制4次，合并成一张4K大图
echo 2. 将对应的蒙版也复制4次，合并成一张大蒙版
echo 3. 在合并后的大图上提取完整元素
echo.

:: 检查是否有配置文件
if exist "config.ini" (
    echo 检测到配置文件 config.ini
    echo 配置文件中的 [4图合并提取元素] 节包含以下设置：
    echo.
    
    :: 显示配置文件中的设置
    for /f "tokens=1,* delims==" %%a in ('type config.ini ^| findstr /v "^#" ^| findstr /v "^$" ^| findstr /i "\[4图合并提取元素\] RGBA_PATH MASK_PATH OUTPUT_DIR MIN_AREA"') do (
        if "%%a"=="RGBA_PATH" (
            echo RGBA_PATH: %%b
        ) else if "%%a"=="MASK_PATH" (
            echo MASK_PATH: %%b
        ) else if "%%a"=="OUTPUT_DIR" (
            echo OUTPUT_DIR: %%b
        ) else if "%%a"=="MIN_AREA" (
            echo MIN_AREA: %%b
        )
    )
    
    echo.
    set /p "USE_CONFIG=是否从配置文件读取参数? (Y/N) [默认Y]: " || set USE_CONFIG=Y
    
    if /i "!USE_CONFIG!"=="Y" (
        echo.
        echo 正在从配置文件读取参数...
        python grid_split_elements.py
        
        if !errorlevel! equ 0 (
            echo.
            echo 处理完成！
            echo 请查看输出目录中的结果文件。
        ) else (
            echo.
            echo 处理过程中出现错误！
            echo 请检查配置文件中的路径设置是否正确。
        )
        
        echo.
        echo 按任意键退出...
        pause > nul
        exit /b 0
    )
)

echo 使用交互式输入模式...
echo.

:: 获取透明图片路径
echo 请输入四方连续透明图片路径（或拖拽文件到此处）
set /p "RGBA_PATH=透明图片路径: "
set RGBA_PATH=%RGBA_PATH:"=%

:: 检查文件是否存在
if not exist "%RGBA_PATH%" (
    echo 错误：找不到透明图片文件！
    pause
    exit /b 1
)

:: 自动推断蒙版文件路径
for %%F in ("%RGBA_PATH%") do (
    set "DIR=%%~dpF"
    set "NAME=%%~nF"
    set "EXT=%%~xF"
)

:: 尝试不同的蒙版文件命名模式
set "MASK_PATH="
if exist "%DIR%%NAME:_rgba=_mask%%EXT%" (
    set "MASK_PATH=%DIR%%NAME:_rgba=_mask%%EXT%"
) else if exist "%DIR%%NAME%_mask%EXT%" (
    set "MASK_PATH=%DIR%%NAME%_mask%EXT%"
)

:: 如果没有自动找到，手动输入
if not defined MASK_PATH (
    echo.
    echo 未能自动找到对应的蒙版文件
    set /p "MASK_PATH=请输入蒙版图片路径（或拖拽文件到此处）: "
    set MASK_PATH=!MASK_PATH:"=!
) else (
    echo 自动找到蒙版文件: %MASK_PATH%
    set /p "USE_AUTO=使用此文件吗? (Y/N) [默认Y]: " || set USE_AUTO=Y
    if /i "!USE_AUTO!" neq "Y" (
        set /p "MASK_PATH=请输入蒙版图片路径（或拖拽文件到此处）: "
        set MASK_PATH=!MASK_PATH:"=!
    )
)

:: 检查蒙版文件是否存在
if not exist "%MASK_PATH%" (
    echo 错误：找不到蒙版文件！
    pause
    exit /b 1
)

:: 设置输出目录
echo.
set /p "CUSTOM_OUTPUT=是否自定义输出目录? (Y/N) [默认N，使用 %OUTPUT_DIR%]: " || set CUSTOM_OUTPUT=N
if /i "%CUSTOM_OUTPUT%"=="Y" (
    set /p "OUTPUT_DIR=请输入输出目录路径: "
)

:: 设置最小面积阈值
echo.
set /p "CUSTOM_MIN_AREA=是否自定义最小元素面积? (Y/N) [默认N，使用 %MIN_AREA%]: " || set CUSTOM_MIN_AREA=N
if /i "%CUSTOM_MIN_AREA%"=="Y" (
    set /p "MIN_AREA=请输入最小面积阈值 (像素): "
)

:: 执行处理
echo.
echo ========================================
echo 开始处理...
echo 透明图片: %RGBA_PATH%
echo 蒙版图片: %MASK_PATH%
echo 输出目录: %OUTPUT_DIR%
echo 最小面积: %MIN_AREA%
echo ========================================
echo.

:: 创建临时目录用于存放复制的图片
set "TEMP_DIR=%TEMP%\rmbg_merge_temp"
if exist "%TEMP_DIR%" rmdir /s /q "%TEMP_DIR%"
mkdir "%TEMP_DIR%"

:: 复制图片到临时目录
copy "%RGBA_PATH%" "%TEMP_DIR%\rgba_0.png" >nul
copy "%RGBA_PATH%" "%TEMP_DIR%\rgba_1.png" >nul
copy "%RGBA_PATH%" "%TEMP_DIR%\rgba_2.png" >nul
copy "%RGBA_PATH%" "%TEMP_DIR%\rgba_3.png" >nul

copy "%MASK_PATH%" "%TEMP_DIR%\mask_0.png" >nul
copy "%MASK_PATH%" "%TEMP_DIR%\mask_1.png" >nul
copy "%MASK_PATH%" "%TEMP_DIR%\mask_2.png" >nul
copy "%MASK_PATH%" "%TEMP_DIR%\mask_3.png" >nul

:: 调用Python脚本进行合并和提取
python grid_split_elements.py --rgba-paths "%TEMP_DIR%\rgba_0.png" "%TEMP_DIR%\rgba_1.png" "%TEMP_DIR%\rgba_2.png" "%TEMP_DIR%\rgba_3.png" --mask-paths "%TEMP_DIR%\mask_0.png" "%TEMP_DIR%\mask_1.png" "%TEMP_DIR%\mask_2.png" "%TEMP_DIR%\mask_3.png" --output "%OUTPUT_DIR%" --min-area %MIN_AREA%

:: 清理临时文件
rmdir /s /q "%TEMP_DIR%" 2>nul

:: 检查是否成功
if !errorlevel! equ 0 (
    echo.
    echo 处理完成！
    echo 输出文件保存在: %OUTPUT_DIR%
    
    :: 打开输出文件夹
    start "" "%OUTPUT_DIR%"
) else (
    echo.
    echo 处理过程中出现错误！
)

:: 等待用户确认
echo.
echo 按任意键退出...
pause > nul
