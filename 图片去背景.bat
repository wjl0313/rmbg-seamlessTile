@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

:: 激活虚拟环境
call .\venv\Scripts\activate

:: 检查是否已登录
if not defined HUGGING_FACE_HUB_TOKEN (
    echo 错误：未检测到Hugging Face登录令牌！
    echo 请先运行 登录配置.bat 完成登录设置。
    pause
    exit /b 1
)

:: 读取配置文件中的参数
for /f "tokens=1,* delims==" %%a in ('type config.ini ^| findstr /v "^#" ^| findstr /v "^$" ^| findstr /i "\[图片去背景\] INPUT_PATH OUTPUT_PATH SAVE_BOTH INPUT_SIZE"') do (
    set "%%a=%%b"
)

:: 运行模型
echo 正在处理图片，请稍候...
if "%SAVE_BOTH%"=="true" (
    python run_rmbg.py --input "%INPUT_PATH%" --output "%OUTPUT_PATH%" --both --size %INPUT_SIZE%
) else (
    python run_rmbg.py --input "%INPUT_PATH%" --output "%OUTPUT_PATH%" --size %INPUT_SIZE%
)

:: 检查是否运行成功
if !errorlevel! equ 0 (
    echo 处理完成！
    echo 输出文件已保存到: %OUTPUT_PATH%
) else (
    echo 处理过程中出现错误，请检查配置和环境。
    echo 如果是授权错误，请重新运行 登录配置.bat
)

:: 等待用户确认
echo.
echo 按任意键退出...
pause > nul