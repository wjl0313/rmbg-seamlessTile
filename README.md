# RMBG-SeamlessTile - 图片去背景与四方连续元素提取工具

一个专门处理四方连续图片的Python工具集，支持AI驱动的图片去背景和智能元素提取功能。主要用于无缝贴图、纹理素材等四方连续图案的处理。

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

### 📍 精确坐标定位
- 自动记录元素在原图中的精确坐标
- 文件名包含完整的定位信息
- 支持后续编辑和精确定位

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Windows/Linux/macOS

### 安装依赖
```bash
pip install -r requirements.txt
```

### 使用方法

1. **配置参数**
   - 编辑 `config.ini` 文件设置输入输出路径
   - 运行 `token配置.bat` 完成授权设置

2. **图片去背景**
   ```bash
   # 运行批处理文件
   图片去背景.bat
   ```

3. **元素提取**
   ```bash
   # 运行批处理文件
   4图合并提取元素.bat
   ```

## 📁 项目结构

```
rmbg-seamlessTile/
├── input/                    # 输入图片目录
├── output/                   # 输出结果目录
├── config.ini               # 配置文件
├── run_rmbg.py             # 去背景核心代码
├── grid_split_elements.py  # 元素提取核心代码
├── requirements.txt         # Python依赖
└── *.bat                   # Windows批处理文件
```

## 🔧 配置说明

### 图片去背景配置
```ini
[图片去背景]
INPUT_PATH=input/test.png      # 输入图片路径
OUTPUT_PATH=output/rmbg_output # 输出目录
SAVE_BOTH=true                # 是否同时输出蒙版和透明图
INPUT_SIZE=1024               # 模型输入尺寸
```

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
- `elements_info.txt` - 元素位置信息汇总

### 元素命名格式
```
element_000_orig_x10_y20_w50_h60.png
```
- `000` - 元素索引
- `x10_y20` - 原图坐标
- `w50_h60` - 元素尺寸

## 🎯 使用场景

- **四方连续贴图处理** - 处理无缝贴图、纹理素材
- **图案元素提取** - 从四方连续图案中提取完整元素
- **素材库管理** - 批量提取和管理四方连续图案元素
- **纹理设计** - 处理需要无缝拼接的纹理图案

## 🔍 技术特点

- **AI驱动** - 使用最新的RMBG-2.0模型
- **智能检测** - 自动识别和提取图像元素
- **坐标精确** - 保持元素的精确定位信息
- **跨平台** - 支持Windows、Linux、macOS
- **配置灵活** - 通过配置文件轻松调整参数

## 📝 注意事项

- 输入图片应为四方连续图案以获得最佳效果
- 首次运行会自动下载AI模型文件
- 建议使用1024x1024或更高分辨率的图片
- 透明图片和蒙版图片尺寸必须一致

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 📄 许可证

本项目采用MIT许可证，详见LICENSE文件。

---

**让四方连续图案处理变得更简单！** 🔄✨
