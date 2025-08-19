# RMBG-SeamlessTile - Background Removal & Seamless Tile Element Extraction Tool

A Python toolkit specifically designed for seamless tile processing, featuring AI-powered background removal and intelligent element extraction. Mainly used for seamless textures, pattern materials, and other seamless tile images.

## ✨ Key Features

### 🎨 AI Background Removal
- Based on **RMBG-2.0** official model
- Customizable input size and output formats
- Simultaneous output of transparent images and masks
- One-click batch processing

### 🔄 Seamless Tile Processing
- Automatic 2x2 tile replication and merging
- Generates 4K resolution (2048x2048) complete pattern display
- Intelligent element detection and extraction
- Maintains element integrity and continuity

### 📍 Precise Coordinate Positioning
- Automatic recording of element coordinates in original images
- Filenames contain complete positioning information
- Supports subsequent editing and precise positioning

## 🚀 Quick Start

### Requirements
- Python 3.8+
- Windows/Linux/macOS

### Installation
```bash
pip install -r requirements.txt
```

### Usage

1. **Configure Parameters**
   - Edit `config.ini` file to set input/output paths
   - Run `token配置.bat` to complete authorization

2. **Background Removal**
   ```bash
   图片去背景.bat
   ```

3. **Element Extraction**
   ```bash
   4图合并提取元素.bat
   ```

## 📁 Project Structure

```
rmbg-seamlessTile/
├── input/                    # Input images directory
├── output/                   # Output results directory
├── config.ini               # Configuration file
├── run_rmbg.py             # Background removal core code
├── grid_split_elements.py  # Element extraction core code
├── requirements.txt         # Python dependencies
└── *.bat                   # Windows batch files
```

## 🔧 Configuration

### Background Removal Config
```ini
[图片去背景]
INPUT_PATH=input/test.png      # Input image path
OUTPUT_PATH=output/rmbg_output # Output directory
SAVE_BOTH=true                # Output both mask and transparent image
INPUT_SIZE=1024               # Model input size
```

### Element Extraction Config
```ini
[4图合并提取元素]
RGBA_PATH=output/rmbg_output/rgba.png  # Transparent image path
MASK_PATH=output/rmbg_output/mask.png  # Mask image path
OUTPUT_DIR=output/merged_output        # Output directory
MIN_AREA=10                           # Minimum element area threshold
```

## 📊 Output Files

### Background Removal Output
- `原文件名_rgba.png` - Transparent background image
- `原文件名_mask.png` - Mask image

### Element Extraction Output
- `merged_rgba.png` - Merged 4K transparent image
- `merged_mask.png` - Merged 4K mask image
- `elements/` - Extracted elements folder
- `elements_info.txt` - Element position information summary

### Element Naming Format
```
element_000_orig_x10_y20_w50_h60.png
```
- `000` - Element index
- `x10_y20` - Original image coordinates
- `w50_h60` - Element dimensions

## 🎯 Use Cases

- **Seamless Tile Processing** - Handle seamless textures and pattern materials
- **Pattern Element Extraction** - Extract complete elements from seamless patterns
- **Asset Library Management** - Batch extract and manage seamless tile elements
- **Texture Design** - Process textures that require seamless tiling

## 🔍 Technical Features

- **AI-Powered** - Uses latest RMBG-2.0 model
- **Smart Detection** - Automatic element recognition and extraction
- **Precise Coordinates** - Maintains accurate element positioning
- **Cross-Platform** - Supports Windows, Linux, macOS
- **Flexible Configuration** - Easy parameter adjustment via config file

## 📝 Notes

- Input images should be seamless tiles for best results
- AI models are automatically downloaded on first run
- Recommended image resolution: 1024x1024 or higher
- Transparent and mask images must have identical dimensions

## 🤝 Contributing

Issues and Pull Requests are welcome!

## 📄 License

This project is licensed under the MIT License.

---

**Making seamless tile processing simpler!** 🔄✨
