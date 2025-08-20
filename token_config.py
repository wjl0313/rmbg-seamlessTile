#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跨平台Hugging Face Token配置脚本
支持Windows和Linux系统
"""

import os
import sys
import platform
import subprocess
from pathlib import Path

def print_header():
    """打印脚本头部信息"""
    print("=" * 60)
    print("🤗 Hugging Face Token 配置工具")
    print("支持 Windows 和 Linux 系统")
    print("=" * 60)
    print()

def check_python():
    """检查Python环境"""
    print("🔍 检查Python环境...")
    if sys.version_info < (3, 8):
        print("❌ 错误: 需要Python 3.8或更高版本")
        print(f"   当前版本: {sys.version}")
        sys.exit(1)
    print(f"✅ Python版本: {sys.version.split()[0]}")
    print()

def check_venv():
    """检查虚拟环境"""
    print("🔍 检查虚拟环境...")
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ 虚拟环境已激活")
        return True
    else:
        print("⚠️  未检测到虚拟环境")
        venv_path = Path("venv")
        if venv_path.exists():
            print("   发现venv目录，尝试激活...")
            return activate_venv()
        else:
            print("   建议先创建虚拟环境")
            return False
    print()

def activate_venv():
    """激活虚拟环境"""
    system = platform.system().lower()
    
    if system == "windows":
        activate_script = "venv\\Scripts\\activate.bat"
        if Path(activate_script).exists():
            print("   在Windows上激活虚拟环境...")
            # 在Windows上，我们需要在子进程中激活
            return True
        else:
            print("   ❌ 未找到Windows激活脚本")
            return False
    elif system in ["linux", "darwin"]:  # Linux或macOS
        activate_script = "venv/bin/activate"
        if Path(activate_script).exists():
            print("   在Linux/macOS上激活虚拟环境...")
            # 在Linux/macOS上，我们可以尝试激活
            try:
                activate_path = Path(activate_script).resolve()
                os.environ['VIRTUAL_ENV'] = str(activate_path.parent.parent)
                os.environ['PATH'] = f"{activate_path.parent}:{os.environ['PATH']}"
                sys.path.insert(0, str(activate_path.parent))
                return True
            except Exception as e:
                print(f"   ⚠️  激活失败: {e}")
                return False
        else:
            print("   ❌ 未找到Linux/macOS激活脚本")
            return False
    else:
        print(f"   ⚠️  不支持的操作系统: {system}")
        return False

def install_huggingface_hub():
    """安装或升级huggingface_hub"""
    print("📦 安装/升级huggingface_hub...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "huggingface_hub"], 
                      check=True, capture_output=True, text=True)
        print("✅ huggingface_hub安装/升级成功")
    except subprocess.CalledProcessError as e:
        print(f"❌ 安装失败: {e}")
        print("   请手动运行: pip install --upgrade huggingface_hub")
        return False
    return True

def get_token():
    """获取用户输入的token"""
    print("🔑 请输入您的Hugging Face Token:")
    print("   1. 访问 https://huggingface.co/settings/tokens")
    print("   2. 创建新的token或复制现有token")
    print("   3. 粘贴到下方:")
    print()
    
    while True:
        token = input("Token: ").strip()
        if token:
            if len(token) > 10:  # 简单的token长度检查
                return token
            else:
                print("❌ Token长度不足，请检查后重新输入")
        else:
            print("❌ Token不能为空，请重新输入")

def set_environment_variable(token):
    """设置环境变量"""
    system = platform.system().lower()
    
    print("🔧 设置环境变量...")
    
    if system == "windows":
        try:
            # Windows上使用setx命令
            subprocess.run(["setx", "HUGGING_FACE_HUB_TOKEN", token], 
                          check=True, capture_output=True, text=True)
            print("✅ Windows环境变量设置成功")
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Windows环境变量设置失败: {e}")
            print("   请手动设置环境变量")
    else:
        # Linux/macOS上添加到shell配置文件
        shell_configs = [
            os.path.expanduser("~/.bashrc"),
            os.path.expanduser("~/.zshrc"),
            os.path.expanduser("~/.profile")
        ]
        
        export_line = f'export HUGGING_FACE_HUB_TOKEN="{token}"'
        
        for config_file in shell_configs:
            if os.path.exists(config_file):
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if export_line not in content:
                        with open(config_file, 'a', encoding='utf-8') as f:
                            f.write(f"\n# Hugging Face Token\n{export_line}\n")
                        print(f"✅ 已添加到 {config_file}")
                    else:
                        print(f"✅ {config_file} 中已存在token配置")
                except Exception as e:
                    print(f"⚠️  写入 {config_file} 失败: {e}")
                break
        else:
            print("⚠️  未找到shell配置文件，请手动添加:")
            print(f"   {export_line}")

def login_with_token(token):
    """使用token登录"""
    print("🔐 使用token登录Hugging Face...")
    try:
        login_script = f"""
from huggingface_hub import login
try:
    login('{token}')
    print("✅ 登录成功！")
except Exception as e:
    print(f"❌ 登录失败: {{e}}")
    sys.exit(1)
"""
        subprocess.run([sys.executable, "-c", login_script], check=True)
        return True
    except subprocess.CalledProcessError:
        print("❌ 登录失败")
        return False

def main():
    """主函数"""
    print_header()
    
    # 检查环境
    check_python()
    venv_activated = check_venv()
    
    if not venv_activated:
        print("⚠️  虚拟环境未激活，继续执行...")
    
    # 安装依赖
    if not install_huggingface_hub():
        sys.exit(1)
    
    # 获取token
    token = get_token()
    
    # 设置环境变量
    set_environment_variable(token)
    
    # 登录
    if not login_with_token(token):
        sys.exit(1)
    
    print()
    print("🎉 配置完成！")
    print("现在您可以运行图片处理脚本了")
    print()
    
    if platform.system().lower() == "windows":
        input("按回车键退出...")
    else:
        print("脚本执行完成")

if __name__ == "__main__":
    main()
