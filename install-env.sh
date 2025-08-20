#!/bin/bash
# 图片去背景项目环境配置脚本
# 适用于 Linux 和 macOS

# 设置错误处理
set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${CYAN}[信息]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[成功]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[警告]${NC} $1"
}

print_error() {
    echo -e "${RED}[错误]${NC} $1"
}

print_header() {
    echo -e "${CYAN}========================================"
    echo -e "$1"
    echo -e "========================================${NC}"
}

print_header "开始环境配置 - 图片去背景项目"
echo ""

# 检测Python
print_info "检测Python环境..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    print_error "未检测到Python，请先安装Python 3.8+"
    echo "Ubuntu/Debian: sudo apt install python3 python3-venv python3-pip"
    echo "CentOS/RHEL: sudo yum install python3 python3-venv python3-pip"
    echo "macOS: brew install python3"
    echo "下载地址：https://www.python.org/downloads/"
    read -p "按回车键退出"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
print_success "Python已安装"
echo "版本: $PYTHON_VERSION"

# 检测GPU环境
echo ""
print_info "检测GPU环境..."

if command -v nvidia-smi &> /dev/null; then
    GPU_INFO=$(nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader,nounits 2>/dev/null)
    if [ $? -eq 0 ]; then
        print_success "检测到NVIDIA GPU"
        echo "GPU详情："
        echo "$GPU_INFO"
        HAS_GPU=true
    else
        print_error "nvidia-smi执行失败"
        HAS_GPU=false
    fi
else
    print_error "未检测到NVIDIA GPU或nvidia-smi命令"
    HAS_GPU=false
fi

if [ "$HAS_GPU" != "true" ]; then
    echo ""
    print_error "本项目需要NVIDIA GPU支持，无法在CPU环境下运行"
    echo "请确保："
    echo "1. 安装了NVIDIA显卡驱动"
    echo "2. 显卡支持CUDA计算"
    echo "3. 系统环境变量配置正确"
    echo ""
    echo "如果没有GPU设备，请使用其他支持CPU的图片处理工具"
    read -p "按回车键退出"
    exit 1
fi

# 检测CUDA版本
echo ""
print_info "检测CUDA版本..."
if command -v nvcc &> /dev/null; then
    CUDA_VERSION=$(nvcc --version 2>&1 | head -n1)
    print_success "CUDA Toolkit已安装"
    echo "版本: $CUDA_VERSION"
else
    print_warning "未检测到CUDA Toolkit"
    echo "说明: 不影响PyTorch GPU版本安装，会使用预编译版本"
fi

# 检测pip
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    print_error "未检测到pip，请先安装pip"
    echo "Ubuntu/Debian: sudo apt install python3-pip"
    echo "CentOS/RHEL: sudo yum install python3-pip"
    echo "macOS: brew install python3"
    read -p "按回车键退出"
    exit 1
fi

# 设置pip命令
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
else
    PIP_CMD="pip"
fi

# 创建虚拟环境
echo ""
print_info "创建Python虚拟环境..."
if [ -d "venv" ]; then
    print_warning "虚拟环境已存在，是否删除重建？(y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        rm -rf venv
        print_info "已删除旧虚拟环境"
    else
        print_warning "使用现有虚拟环境"
    fi
fi

if [ ! -d "venv" ]; then
    $PYTHON_CMD -m venv venv
    if [ $? -ne 0 ]; then
        print_error "创建虚拟环境失败"
        read -p "按回车键退出"
        exit 1
    fi
    print_success "虚拟环境创建成功"
fi

# 激活虚拟环境
echo ""
print_info "激活虚拟环境..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    print_error "激活虚拟环境失败"
    read -p "按回车键退出"
    exit 1
fi
print_success "虚拟环境激活成功"

# 升级pip
echo ""
print_info "升级pip..."
python -m pip install --upgrade pip
print_success "pip升级成功"

# 安装GPU版本的PyTorch
echo ""
print_info "安装GPU版本的PyTorch..."
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
if [ $? -ne 0 ]; then
    print_error "安装GPU版本PyTorch失败"
    echo "请检查网络连接或手动安装"
    read -p "按回车键退出"
    exit 1
fi
print_success "PyTorch GPU版本安装成功"

# 验证PyTorch CUDA支持
echo ""
print_info "验证PyTorch CUDA支持..."
python -c "
import torch
print(f'PyTorch版本: {torch.__version__}')
print(f'CUDA可用: {torch.cuda.is_available()}')
print(f'CUDA版本: {torch.version.cuda}')
print(f'GPU数量: {torch.cuda.device_count()}')
"

# 安装其他依赖
echo ""
print_info "安装其他项目依赖..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    print_error "安装项目依赖失败"
    read -p "按回车键退出"
    exit 1
fi
print_success "项目依赖安装成功"

# 安装完成提示
echo ""
print_header "环境配置完成！(GPU版本)"
echo ""
echo "已安装的组件："
echo "- Python虚拟环境 (venv)"
echo "- GPU版本PyTorch (支持CUDA加速)"
echo "- 所有项目依赖包"
echo ""
echo "现在您可以享受GPU加速带来的快速图片处理！"
echo ""
echo "使用方法："
echo "1. 激活环境: source venv/bin/activate"
echo "2. 运行项目: python run_rmbg.py"
echo "3. 退出环境: deactivate"
echo ""
read -p "按回车键完成安装"
