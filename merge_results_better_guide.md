# 结果合并脚本使用说明

## 概述
`merge_results_better.py` 是一个用于合并图片处理结果的脚本，它将颜色分析和元素提取的结果合并到一张1536x1536的图片中。

## 功能特性
- 自动加载背景颜色（从 `colors_output.json`）
- 自动加载元素信息（从 `elements_output.json`）
- 强制修复BGR到RGB通道问题
- 保持透明度信息
- 自动调整元素尺寸以匹配边界框

## 文件依赖
- **输入文件**：
  - `output/merged_output/colors_output.json` - 颜色分析结果
  - `output/merged_output/elements_output.json` - 元素提取结果
- **输出文件**：
  - `output/merged_final_better.png` - 合并后的最终图片

## 使用方法

### 1. 直接运行
```bash
python merge_results_better.py
```

### 2. 作为流水线的一部分
在 `run_pipeline.bat` 或 `run_pipeline.sh` 中添加：
```bash
python merge_results_better.py
```

## 技术细节

### 通道修复
脚本会自动检测并修复BGR到RGB的通道顺序问题：
- 强制交换R和B通道
- 确保颜色显示正确
- 保持透明度信息

### 图片处理流程
1. 加载背景颜色并创建1536x1536的背景图片
2. 解析每个元素的边界框坐标
3. 将base64编码的元素图片转换为PIL Image对象
4. 调整元素尺寸以匹配边界框
5. 将元素粘贴到背景图片上
6. 保存最终结果

## 输出说明
- **背景颜色**：使用 `colors_output.json` 中的 `backgroundColor1`
- **元素位置**：根据 `elements_output.json` 中的 `bbox` 坐标
- **透明度**：保持原始元素的alpha通道信息
- **图片格式**：PNG格式，支持透明度

## 注意事项
- 确保输入文件存在且格式正确
- 脚本会自动创建输出目录
- 如果元素坐标超出图片范围，该元素会被跳过
- 建议在运行前确保所有依赖脚本已完成

## 故障排除

### 常见问题
1. **文件不存在错误**：检查输入文件路径是否正确
2. **颜色显示异常**：脚本已自动修复通道问题
3. **元素位置错误**：检查 `bbox` 坐标格式是否正确

### 调试信息
脚本会输出详细的处理信息，包括：
- 背景颜色值
- 加载的元素数量
- 每个元素的处理状态
- 最终输出路径

## 相关脚本
- `run_rmbg.py` - 背景去除
- `color_analyzer.py` - 颜色分析
- `grid_split_elements.py` - 元素提取
- `run_pipeline.bat/sh` - 流水线执行
