# 颜色分析脚本使用说明

本项目提供了颜色分析功能，可以分析config.ini中设置的图片路径，获取占比最大的颜色并返回16进制色值。

## 📁 文件说明

### 1. **color_analyzer.py** - 核心颜色分析器
- **功能**: 主要的颜色分析类
- **特性**: 支持批量分析、单张分析、综合统计
- **依赖**: PIL, numpy, configparser

### 2. **analyze_colors.py** - 使用示例脚本
- **功能**: 演示如何使用ColorAnalyzer类
- **用途**: 学习和测试颜色分析功能

## 🚀 快速开始

### 基本使用

```python
from color_analyzer import ColorAnalyzer

# 创建分析器实例
analyzer = ColorAnalyzer("config.ini")

# 分析所有图片
results = analyzer.analyze_all_images(num_colors=3)

# 获取综合主要颜色
dominant_colors = analyzer.get_dominant_colors_summary(num_colors=3)
```

### 命令行使用

```bash
# 分析所有图片的详细颜色
python color_analyzer.py

# 显示综合主要颜色
python color_analyzer.py --summary

# 指定配置文件路径
python color_analyzer.py --config my_config.ini

# 指定返回颜色数量
python color_analyzer.py --num-colors 5
```

## 🔧 主要功能

### 1. **自动图片路径检测**
- 自动扫描config.ini中的所有配置节
- 智能识别图片文件路径
- 支持多种图片格式：PNG, JPG, JPEG, BMP, GIF, TIFF, WEBP

### 2. **颜色分析算法**
- 使用像素级统计方法
- 支持RGB颜色空间
- 自动转换为16进制色值
- 计算颜色占比百分比

### 3. **批量处理能力**
- 同时分析多张图片
- 生成详细的分析报告
- 支持综合颜色权重统计

## 📊 输出格式

### 单张图片分析结果
```python
[
    ('#FF0000', 25.50),  # 红色，占比25.50%
    ('#00FF00', 20.30),  # 绿色，占比20.30%
    ('#0000FF', 15.20)   # 蓝色，占比15.20%
]
```

### 批量分析结果
```python
{
    'input/test.png': [
        ('#FF0000', 25.50),
        ('#00FF00', 20.30),
        ('#0000FF', 15.20)
    ],
    'input/another.png': [
        ('#FFFF00', 30.10),
        ('#FF00FF', 18.50),
        ('#00FFFF', 12.80)
    ]
}
```

## 🎯 使用场景

### 1. **设计分析**
- 分析图片的配色方案
- 提取主要颜色用于设计参考
- 统计颜色使用频率

### 2. **素材管理**
- 为图片库添加颜色标签
- 按颜色分类管理素材
- 快速找到特定色调的图片

### 3. **质量检测**
- 检测图片是否偏色
- 分析颜色分布是否合理
- 评估图片的视觉平衡

## ⚙️ 配置要求

### 配置文件格式
```ini
[图片去背景]
INPUT_PATH=input/test.png      # 输入图片路径
OUTPUT_PATH=output/rmbg_output # 输出目录

[4图合并提取元素]
RGBA_PATH=output/rgba.png     # 透明图片路径
MASK_PATH=output/mask.png     # 蒙版图片路径
```

### 支持的图片格式
- **PNG** - 推荐，支持透明通道
- **JPG/JPEG** - 常用格式
- **BMP** - 无压缩格式
- **GIF** - 动画支持
- **TIFF** - 高质量格式
- **WEBP** - 现代格式

## 🔍 技术特点

### 1. **高效算法**
- 使用numpy进行快速数组操作
- 像素级统计，精确度高
- 内存友好的处理方式

### 2. **智能识别**
- 自动检测图片文件路径
- 支持相对路径和绝对路径
- 错误处理和异常恢复

### 3. **灵活配置**
- 可自定义返回颜色数量
- 支持不同配置文件
- 命令行参数支持

## 📝 注意事项

### 1. **性能考虑**
- 大图片处理时间较长
- 建议图片尺寸不超过4096x4096
- 内存使用与图片大小成正比

### 2. **颜色精度**
- RGB颜色空间，8位精度
- 相似颜色可能被分别统计
- 建议结合颜色聚类算法

### 3. **文件要求**
- 确保图片文件存在且可读
- 支持常见图片格式
- 建议使用RGB模式的图片

## 🚨 故障排除

### 常见问题

1. **配置文件不存在**
   - 检查config.ini文件路径
   - 确保文件编码为UTF-8

2. **图片路径无效**
   - 检查图片文件是否存在
   - 确认路径格式正确

3. **分析失败**
   - 检查图片格式是否支持
   - 确认图片文件未损坏

### 调试建议

```python
# 启用详细日志
import logging
logging.basicConfig(level=logging.DEBUG)

# 检查配置加载
analyzer = ColorAnalyzer("config.ini")
print(f"配置加载状态: {analyzer.config is not None}")

# 检查图片路径
paths = analyzer.get_image_paths_from_config()
print(f"找到的图片路径: {paths}")
```

## 🤝 扩展功能

### 1. **颜色聚类**
- 合并相似颜色
- 减少颜色数量
- 提高分析精度

### 2. **颜色空间转换**
- 支持HSV颜色空间
- 支持LAB颜色空间
- 更符合人眼感知

### 3. **批量导出**
- 导出为CSV格式
- 生成颜色报告
- 支持多种输出格式

---

**让颜色分析变得更简单！** 🎨✨
