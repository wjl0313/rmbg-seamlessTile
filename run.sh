#!/bin/bash
# 图片处理流水线脚本
# 按顺序执行：去背景 -> 元素提取 -> 颜色分析

set -e  # 遇到错误时退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# 辅助函数
print_header() {
    echo -e "${CYAN}========================================"
    echo -e "$1"
    echo -e "========================================${NC}"
}

print_info() {
    echo -e "${YELLOW}[信息] $1${NC}"
}

print_success() {
    echo -e "${GREEN}[成功] $1${NC}"
}

print_error() {
    echo -e "${RED}[错误] $1${NC}"
}

# 检查Python环境
check_python() {
    print_info "检查Python环境..."
    if ! command -v python3 &> /dev/null; then
        if ! command -v python &> /dev/null; then
            print_error "未找到Python，请先安装Python 3.8+"
            exit 1
        else
            PYTHON_CMD="python"
        fi
    else
        PYTHON_CMD="python3"
    fi
    print_success "使用Python命令: $PYTHON_CMD"
}

# 检查虚拟环境
check_venv() {
    print_info "检查虚拟环境..."
    if [ -f "venv/bin/activate" ]; then
        print_info "激活虚拟环境..."
        source venv/bin/activate
        print_success "虚拟环境已激活"
    else
        print_info "未检测到虚拟环境，使用系统Python"
    fi
}

# 检查配置文件
check_config() {
    print_info "检查配置文件..."
    if [ ! -f "config.json" ]; then
        print_error "配置文件config.json不存在"
        exit 1
    fi
    print_success "配置文件检查通过"
}

# 执行去背景处理
run_background_removal() {
    print_header "步骤1: 执行图片去背景"
    
    print_info "运行rmbg.py..."
    if $PYTHON_CMD rmbg.py; then
        print_success "去背景处理完成"
    else
        print_error "去背景处理失败"
        exit 1
    fi
}

# 执行元素提取
run_element_extraction() {
    print_header "步骤2: 执行元素提取"
    
    print_info "运行grid_split_elements.py..."
    if $PYTHON_CMD grid_split_elements.py; then
        print_success "元素提取完成"
    else
        print_error "元素提取失败"
        exit 1
    fi
}

# 执行颜色分析
run_color_analysis() {
    print_header "步骤3: 执行颜色分析"
    
    print_info "运行color_analyzer.py..."
    if $PYTHON_CMD color_analyzer.py --summary; then
        print_success "颜色分析完成"
    else
        print_error "颜色分析失败"
        exit 1
    fi
}

# 主函数
main() {
    print_header "开始执行图片处理流水线"
    
    # 环境检查
    check_python
    check_venv
    check_config
    
    # 执行流水线
    run_background_removal
    run_element_extraction
    run_color_analysis
    
    print_header "流水线执行完成"
    print_success "所有步骤已成功完成！"
    echo
    echo "各脚本的输出文件请查看对应脚本的说明文档"
}

# 执行主函数
main "$@"
