#!/usr/bin/env pwsh
# 图片去背景项目环境配置脚本
# 支持 Windows 和 Linux/macOS

# 设置错误处理
$ErrorActionPreference = "Stop"

# 检测操作系统
$isWindows = $IsWindows -or $env:OS -eq "Windows_NT"
$isLinux = $IsLinux -or $env:OS -eq "Unix"
$isMacOS = $IsMacOS

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "开始环境配置 - 图片去背景项目" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检测Python
Write-Host "[检测] Python环境..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[状态] ✅ Python已安装" -ForegroundColor Green
        Write-Host "[版本] $pythonVersion" -ForegroundColor White
    } else {
        throw "Python未安装"
    }
} catch {
    Write-Host "[错误] 未检测到Python，请先安装Python 3.8+" -ForegroundColor Red
    Write-Host "下载地址：https://www.python.org/downloads/" -ForegroundColor White
    if ($isWindows) {
        Write-Host "安装时请勾选 'Add Python to PATH'" -ForegroundColor Yellow
    }
    Read-Host "按回车键退出"
    exit 1
}

# 检测GPU环境
Write-Host ""
Write-Host "[检测] GPU环境..." -ForegroundColor Yellow

$hasGPU = $false
$gpuInfo = ""

if ($isWindows) {
    # Windows GPU检测
    try {
        $gpuInfo = nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader,nounits 2>&1
        if ($LASTEXITCODE -eq 0) {
            $hasGPU = $true
            Write-Host "[状态] ✅ 检测到NVIDIA GPU" -ForegroundColor Green
            Write-Host "[信息] GPU详情：" -ForegroundColor White
            Write-Host $gpuInfo -ForegroundColor White
        } else {
            throw "nvidia-smi执行失败"
        }
    } catch {
        Write-Host "[状态] ❌ 未检测到NVIDIA GPU" -ForegroundColor Red
    }
} else {
    # Linux/macOS GPU检测
    try {
        $gpuInfo = nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader,nounits 2>&1
        if ($LASTEXITCODE -eq 0) {
            $hasGPU = $true
            Write-Host "[状态] ✅ 检测到NVIDIA GPU" -ForegroundColor Green
            Write-Host "[信息] GPU详情：" -ForegroundColor White
            Write-Host $gpuInfo -ForegroundColor White
        } else {
            throw "nvidia-smi执行失败"
        }
    } catch {
        Write-Host "[状态] ❌ 未检测到NVIDIA GPU" -ForegroundColor Red
    }
}

if (-not $hasGPU) {
    Write-Host ""
    Write-Host "[错误] 本项目需要NVIDIA GPU支持，无法在CPU环境下运行" -ForegroundColor Red
    Write-Host "请确保：" -ForegroundColor White
    Write-Host "1. 安装了NVIDIA显卡驱动" -ForegroundColor White
    Write-Host "2. 显卡支持CUDA计算" -ForegroundColor White
    Write-Host "3. 系统环境变量配置正确" -ForegroundColor White
    Write-Host ""
    Write-Host "如果没有GPU设备，请使用其他支持CPU的图片处理工具" -ForegroundColor Yellow
    Read-Host "按回车键退出"
    exit 1
}

# 检测CUDA版本
Write-Host ""
Write-Host "[检测] CUDA版本..." -ForegroundColor Yellow
try {
    $cudaVersion = nvcc --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[状态] ✅ CUDA Toolkit已安装" -ForegroundColor Green
        Write-Host "[版本] $cudaVersion" -ForegroundColor White
    } else {
        Write-Host "[状态] ⚠️  未检测到CUDA Toolkit" -ForegroundColor Yellow
        Write-Host "[说明] 不影响PyTorch GPU版本安装，会使用预编译版本" -ForegroundColor White
    }
} catch {
    Write-Host "[状态] ⚠️  未检测到CUDA Toolkit" -ForegroundColor Yellow
    Write-Host "[说明] 不影响PyTorch GPU版本安装，会使用预编译版本" -ForegroundColor White
}

# 创建虚拟环境
Write-Host ""
Write-Host "[信息] 创建Python虚拟环境..." -ForegroundColor Yellow
try {
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        throw "创建虚拟环境失败"
    }
    Write-Host "[状态] ✅ 虚拟环境创建成功" -ForegroundColor Green
} catch {
    Write-Host "[错误] 创建虚拟环境失败: $_" -ForegroundColor Red
    Read-Host "按回车键退出"
    exit 1
}

# 激活虚拟环境
Write-Host ""
Write-Host "[信息] 激活虚拟环境..." -ForegroundColor Yellow
try {
    if ($isWindows) {
        & ".\venv\Scripts\Activate.ps1"
    } else {
        & ".\venv\bin\Activate.ps1"
    }
    
    if ($LASTEXITCODE -ne 0) {
        throw "激活虚拟环境失败"
    }
    Write-Host "[状态] ✅ 虚拟环境激活成功" -ForegroundColor Green
} catch {
    Write-Host "[错误] 激活虚拟环境失败: $_" -ForegroundColor Red
    Read-Host "按回车键退出"
    exit 1
}

# 升级pip
Write-Host ""
Write-Host "[信息] 升级pip..." -ForegroundColor Yellow
try {
    python.exe -m pip install --upgrade pip
    Write-Host "[状态] ✅ pip升级成功" -ForegroundColor Green
} catch {
    Write-Host "[警告] pip升级失败，继续安装依赖: $_" -ForegroundColor Yellow
}

# 安装GPU版本的PyTorch
Write-Host ""
Write-Host "[信息] 安装GPU版本的PyTorch..." -ForegroundColor Yellow
try {
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
    if ($LASTEXITCODE -ne 0) {
        throw "安装GPU版本PyTorch失败"
    }
    Write-Host "[状态] ✅ PyTorch GPU版本安装成功" -ForegroundColor Green
} catch {
    Write-Host "[错误] 安装失败: $_" -ForegroundColor Red
    Write-Host "请检查网络连接或手动安装" -ForegroundColor Yellow
    Read-Host "按回车键退出"
    exit 1
}

# 验证PyTorch CUDA支持
Write-Host ""
Write-Host "[信息] 验证PyTorch CUDA支持..." -ForegroundColor Yellow
try {
    $torchInfo = python -c "import torch; print(f'PyTorch版本: {torch.__version__}'); print(f'CUDA可用: {torch.cuda.is_available()}'); print(f'CUDA版本: {torch.version.cuda}'); print(f'GPU数量: {torch.cuda.device_count()}')"
    Write-Host $torchInfo -ForegroundColor White
} catch {
    Write-Host "[警告] PyTorch验证失败: $_" -ForegroundColor Yellow
}

# 安装其他依赖
Write-Host ""
Write-Host "[信息] 安装其他项目依赖..." -ForegroundColor Yellow
try {
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        throw "安装项目依赖失败"
    }
    Write-Host "[状态] ✅ 项目依赖安装成功" -ForegroundColor Green
} catch {
    Write-Host "[错误] 安装项目依赖失败: $_" -ForegroundColor Red
    Read-Host "按回车键退出"
    exit 1
}

# 安装完成提示
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "环境配置完成！(GPU版本)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "已安装的组件：" -ForegroundColor White
Write-Host "- Python虚拟环境 (venv)" -ForegroundColor White
Write-Host "- GPU版本PyTorch (支持CUDA加速)" -ForegroundColor White
Write-Host "- 所有项目依赖包" -ForegroundColor White
Write-Host ""
Write-Host "现在您可以享受GPU加速带来的快速图片处理！" -ForegroundColor Green
Write-Host ""
Write-Host "使用方法：" -ForegroundColor White
if ($isWindows) {
    Write-Host "1. 激活环境：.\venv\Scripts\Activate.ps1" -ForegroundColor White
} else {
    Write-Host "1. 激活环境：.\venv\bin\Activate.ps1" -ForegroundColor White
}
Write-Host "2. 运行项目：python run_rmbg.py" -ForegroundColor White
Write-Host "3. 退出环境：deactivate" -ForegroundColor White
Write-Host ""
Read-Host "按回车键完成安装"
