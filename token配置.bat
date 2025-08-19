@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

:: 激活虚拟环境
call .\venv\Scripts\activate

:: 设置固定的 Hugging Face token
set "HF_TOKEN="

:: 设置环境变量
setx HUGGING_FACE_HUB_TOKEN "%HF_TOKEN%"
set "HUGGING_FACE_HUB_TOKEN=%HF_TOKEN%"

:: 安装huggingface_hub
pip install --upgrade huggingface_hub

:: 使用令牌登录
python -c "from huggingface_hub import login; login('%HF_TOKEN%')"

echo.
echo 配置完成！现在您可以运行图片去背景.bat了
echo.
pause