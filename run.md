# 图片处理流水线使用说明

## 📋 概述

图片处理流水线是一个自动化脚本，按顺序执行以下三个步骤：

1. **图片去背景** (`run_rmbg.py`) - 使用AI模型去除图片背景
2. **颜色分析** (`color_analyzer.py`) - 分析图片的主要颜色
3. **元素提取** (`grid_split_elements.py`) - 从单张图片中提取独立元素

最终输出一个包含所有结果的JSON文件。

## 🚀 快速开始

### 方法1: 使用批处理文件 (Windows)
```bash
# 双击运行
run_pipeline.bat
```

### 方法2: 使用Shell脚本 (Linux/macOS)
```bash
# 添加执行权限
chmod +x run_pipeline.sh

# 运行脚本
./run_pipeline.sh
```

### 方法3: 手动执行
```bash
# 1. 去背景
python run_rmbg.py

# 2. 颜色分析
python color_analyzer.py --summary

# 3. 元素提取
python grid_split_elements.py
```

## 📁 输出文件

### 主要输出
- **`pipeline_results.json`** - 最终结果文件，包含所有处理结果

### 中间文件
- **`output/rmbg_output/`** - 去背景结果
  - `rgba.png` - 透明背景图片
  - `mask.png` - 蒙版图片
- **`output/merged_output/` - 元素提取结果
  - `elements_output.json` - 元素提取的原始结果
  - `elements/` - 提取的独立元素图片

## 📊 结果JSON格式

```json
{
  "masks": [
    {
      "mask": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
      "bbox": [
        "1,2",    // 左上角坐标
        "3,4",    // 右上角坐标
        "4,5",    // 右下角坐标
        "6,7"     // 左下角坐标
      ]
    }
  ],
  "backgroundColor1": [207, 232, 193, 255],  // 主要颜色1 (RGBA)
  "backgroundColor2": [150, 117, 102, 255],  // 主要颜色2 (RGBA)
  "backgroundColor3": [237, 217, 202, 255]   // 主要颜色3 (RGBA)
}
```

## ⚙️ 配置要求

### 1. 配置文件 (`config.json`)
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

### 2. 环境要求
- Python 3.8+
- 虚拟环境 (推荐)
- 必要的Python包 (见 `requirements.txt`)

## 🔧 故障排除

### 常见问题

1. **Python未找到**
   - 确保已安装Python 3.8+
   - 检查PATH环境变量

2. **虚拟环境激活失败**
   - 脚本会自动使用系统Python
   - 手动激活: `.\venv\Scripts\activate` (Windows) 或 `source venv/bin/activate` (Linux/macOS)

3. **配置文件不存在**
   - 确保 `config.json` 文件存在
   - 检查文件路径和权限

4. **输出目录不存在**
   - 脚本会自动创建必要的目录
   - 检查磁盘空间和权限

### 调试模式

如果遇到问题，可以查看临时文件：
- `color_result.txt` - 颜色分析结果
- `element_result.txt` - 元素提取结果

## 📝 自定义配置

### 修改输入图片
编辑 `config.json` 中的 `INPUT_PATH`：
```json
"INPUT_PATH": "input/your_image.png"
```

### 调整元素提取阈值
修改 `MIN_AREA` 值：
```json
"MIN_AREA": 100  // 更大的值会过滤掉小元素
```

### 更改输出目录
修改 `OUTPUT_PATH` 和 `OUTPUT_DIR`：
```json
"OUTPUT_PATH": "custom_output/rmbg",
"OUTPUT_DIR": "custom_output/elements"
```

## 🎯 使用场景

- **游戏开发** - 提取游戏素材元素
- **UI设计** - 分析设计稿的主要颜色
- **图像处理** - 批量处理图片背景
- **素材制作** - 创建无缝贴图素材

## 📞 技术支持

如果遇到问题，请检查：
1. Python版本和依赖包
2. 配置文件格式
3. 输入图片路径
4. 输出目录权限

---

**注意**: 首次运行可能需要下载AI模型，请确保网络连接正常。
