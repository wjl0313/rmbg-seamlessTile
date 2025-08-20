# RMBG-SeamlessTile - 图片去背景与四方连续元素提取工具

<div align="center">

**语言 / Language**: [🇨🇳 中文](README.md) | [🇺🇸 English](README_EN.md)

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-orange?style=flat-square&logo=pytorch)
![OpenCV](https://img.shields.io/badge/OpenCV-Latest-green?style=flat-square&logo=opencv)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=flat-square)

</div>

一个专门处理四方连续图片的Python工具集，支持AI驱动的图片去背景和智能元素提取功能。主要用于无缝贴图、纹理素材等四方连续图案的处理。

## 📋 目录

- [✨ 主要功能](#-主要功能)
- [🚀 快速开始](#-快速开始)
- [🔧 运行项目](#-运行项目)
- [📁 项目结构](#-项目结构)
- [📝 文件命名规范](#-文件命名规范)
- [🔍 技术特点](#-技术特点)
- [🎯 使用场景](#-使用场景)
- [📝 注意事项](#-注意事项)

## ✨ 主要功能

### 🎨 智能图片去背景
- 基于 **RMBG-2.0** 官方模型的AI去背景
- 支持自定义输入尺寸和输出格式
- 同时输出透明图和蒙版图
- 一键批处理，简单易用

### 🔄 四方连续图片处理
- 自动复制并合并四方连续图片（2x2布局）
- 生成4K分辨率（2048x2048）的完整图案展示
- 智能元素检测和提取
- 保持元素的完整性和连续性

### 🎨 智能颜色分析
- 自动分析图片的主要背景颜色
- 提取前3个主要颜色值
- 支持RGBA颜色格式
- 输出JSON格式的颜色数据

### 📍 精确坐标定位
- 自动记录元素在原图中的精确坐标
- 文件名包含完整的定位信息
- 支持后续编辑和精确定位

### 🔗 结果合并与可视化
- 将颜色分析和元素提取结果合并
- 创建1536x1536的背景色图片
- 自动修复BGR到RGB通道问题
- 支持透明度保持和元素精确定位
- 输出最终合并图片 `merged_final_better.png`

## 🚀 快速开始

### 环境要求
- **必须**: NVIDIA显卡（支持CUDA）
- **必须**: Python 3.8+
- **必须**: NVIDIA显卡驱动
- **支持**: Windows 10/11, Linux, macOS

### 🖥️ 跨平台环境安装

#### Windows 系统
```powershell
# 方法1: 使用PowerShell脚本（推荐）
.\install-env.ps1

# 方法2: 手动安装
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
```

#### Linux 系统
```bash
# 方法1: 使用Shell脚本（推荐）
chmod +x install-env.sh
./install-env.sh

# 方法2: 手动安装
python3 -m venv venv
source venv/bin/activate
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
```

#### macOS 系统
```bash
# 方法1: 使用Shell脚本（推荐）
chmod +x install-env.sh
./install-env.sh

# 方法2: 手动安装
python3 -m venv venv
source venv/bin/activate
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
```

### 📋 安装脚本特性

**自动检测功能：**
- ✅ Python环境检测
- ✅ NVIDIA GPU检测
- ✅ CUDA版本检测
- ✅ 自动创建虚拟环境
- ✅ 智能依赖安装

**跨平台支持：**
- 🪟 Windows: PowerShell脚本
- 🐧 Linux: Bash脚本
- 🍎 macOS: Bash脚本

**错误处理：**
- 🚫 无GPU时自动停止安装
- 🔧 详细的错误提示和解决建议
- 📝 完整的安装日志

### 🔧 手动安装依赖
```bash
# 激活虚拟环境后
pip install -r requirements.txt
```

## 🎯 使用方法

### 1. 环境激活
```bash
# Windows
.\venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

### 2. 配置文件设置
项目使用 `config.json` 配置文件来管理各种参数：

```json
{
  "图片去背景": {
    "INPUT_PATH": "input/test.png",
    "OUTPUT_PATH": "output/rmbg_output",
    "SAVE_BOTH": true,
    "INPUT_SIZE": 1024
  },
  "4图合并提取元素": {
    "RGBA_PATH": "output/rmbg_output/rgba.png",
    "MASK_PATH": "output/rmbg_output/mask.png",
    "OUTPUT_DIR": "output/merged_output",
    "MIN_AREA": 50
  }
}
```

**配置说明：**
- `INPUT_PATH`: 输入图片路径
- `OUTPUT_PATH`: 去背景结果输出目录
- `SAVE_BOTH`: 是否同时保存透明图和蒙版图
- `INPUT_SIZE`: 模型输入尺寸
- `RGBA_PATH`: 四方连续透明图片路径
- `MASK_PATH`: 四方连续蒙版图片路径
- `OUTPUT_DIR`: 元素提取输出目录
- `MIN_AREA`: 最小元素面积阈值（像素）

### 3. 运行项目

#### 图片去背景
```bash
# 直接运行Python脚本
python rmbg.py
```

#### 元素提取
```bash
# 直接运行Python脚本
python grid_split_elements.py
```

#### 颜色分析
```bash
# 直接运行Python脚本
python color_analyzer.py --summary
```

#### 结果合并
```bash
# 直接运行Python脚本
python merge_results_better.py

# 或使用批处理文件（Windows）
# 此功能目前只有Python脚本，可直接运行
```

#### 完整流水线
```bash
# 使用Shell脚本（Linux/macOS）
./run.sh
```

### 4. 退出环境
```bash
deactivate
```

## 📁 项目结构

```
rmbg-seamlessTile/
├── input/                    # 输入图片目录
├── output/                   # 输出结果目录
│   ├── rmbg_output/         # 去背景结果
│   └── merged_output/       # 合并输出结果
├── config.json              # 配置文件
├── rmbg.py                 # 去背景核心代码
├── color_analyzer.py       # 颜色分析核心代码
├── grid_split_elements.py  # 元素提取核心代码
├── merge_results_better.py # 结果合并核心代码
├── requirements.txt         # Python依赖
├── install-env.ps1         # Windows环境安装脚本
├── install-env.sh          # Linux/macOS环境安装脚本
├── run.sh                  # Linux/macOS流水线脚本
└── *_guide.md              # 各功能使用说明文档
```

## 🔧 配置说明

### 图片去背景配置
```json
{
  "图片去背景": {
    "INPUT_PATH": "input/test.png",
    "OUTPUT_PATH": "output/rmbg_output",
    "SAVE_BOTH": true,
    "INPUT_SIZE": 1024
  }
}
```

## 📋 文件命名规范

项目采用统一的命名规范，确保Python脚本、批处理文件和说明文档之间的一致性：

### 核心功能模块
- **背景去除**: `rmbg.py` ←→ `rmbg_guide.md`
- **颜色分析**: `color_analyzer.py` ←→ `color_analysis_guide.md`
- **元素提取**: `grid_split_elements.py` ←→ `element_extraction_guide.md`
- **结果合并**: `merge_results_better.py` ←→ `results_merge_guide.md`
- **流水线执行**: `run.sh` ←→ `run.md`

### 命名规则
- **Python脚本**: 使用下划线命名法 (snake_case)
- **说明文档**: 对应功能名称 + `_guide.md`
- 所有文件名使用英文，避免中文字符

详细规范请参考各功能对应的 `*_guide.md` 文档。

### 元素提取配置
```ini
[4图合并提取元素]
RGBA_PATH=output/rmbg_output/rgba.png  # 透明图片路径
MASK_PATH=output/rmbg_output/mask.png  # 蒙版图片路径
OUTPUT_DIR=output/merged_output        # 输出目录
MIN_AREA=10                           # 最小元素面积阈值
```

## 📊 输出文件说明

### 去背景输出
- `原文件名_rgba.png` - 透明背景图片
- `原文件名_mask.png` - 蒙版图片

### 元素提取输出
- `merged_rgba.png` - 合并后的4K透明图
- `merged_mask.png` - 合并后的4K蒙版图
- `elements/` - 提取的元素文件夹
- `elements_output.json` - 元素位置信息（JSON格式）

### 颜色分析输出
- `colors_output.json` - 主要背景颜色（JSON格式）
- 包含 `backgroundColor1`、`backgroundColor2`、`backgroundColor3`

### 元素命名格式
```
element_000.png
```
- `000` - 元素索引（自然数排序）
- 位置信息存储在JSON格式中

### 结果合并输出
- `merged_final_better.png` - 最终合并的1536x1536图片
- 结合背景色和提取的元素
- 保持透明度和精确定位

## 🎯 使用场景

- **四方连续贴图处理** - 处理无缝贴图、纹理素材
- **图案元素提取** - 从四方连续图案中提取完整元素
- **素材库管理** - 批量提取和管理四方连续图案元素
- **纹理设计** - 处理需要无缝拼接的纹理图案

## 🔍 技术特点

- **AI驱动** - 使用最新的RMBG-2.0模型
- **智能检测** - 自动识别和提取图像元素
- **智能颜色分析** - 自动提取主要背景颜色
- **结果合并** - 自动修复BGR到RGB通道问题
- **坐标精确** - 保持元素的精确定位信息
- **跨平台** - 支持Windows、Linux、macOS
- **配置灵活** - 通过配置文件轻松调整参数
- **统一命名** - 跨平台一致的文件命名规范

## 📝 注意事项

- **重要**: 本项目需要NVIDIA GPU支持，无法在CPU环境下运行
- 输入图片应为四方连续图案以获得最佳效果
- 首次运行会自动下载AI模型文件
- 建议使用1024x1024或更高分辨率的图片
- 透明图片和蒙版图片尺寸必须一致

## 🚨 故障排除

### 常见问题

1. **GPU检测失败**
   - 确保安装了NVIDIA显卡驱动
   - 确认显卡支持CUDA计算
   - 重启系统后重试

2. **安装失败**
   - 检查网络连接
   - 尝试使用VPN或代理
   - 手动安装PyTorch GPU版本

3. **CUDA版本不匹配**
   - 使用预编译版本（推荐）
   - 或安装匹配的CUDA Toolkit

### 系统特定问题

**Windows:**
- 确保PowerShell执行策略允许运行脚本
- 以管理员身份运行PowerShell

**Linux:**
- 确保脚本有执行权限：`chmod +x install-env.sh`
- 使用bash shell：`bash install-env.sh`

**macOS:**
- 确保已安装Homebrew（用于安装Python）
- 可能需要允许运行未签名脚本

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 📄 许可证

本项目采用MIT许可证，详见LICENSE文件。

---

**让四方连续图案处理变得更简单！** 🔄✨
