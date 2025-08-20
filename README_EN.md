# RMBG-SeamlessTile - Background Removal & Seamless Tile Element Extraction Tool

<div align="center">

**语言 / Language**: [🇨🇳 中文](README.md) | [🇺🇸 English](README_EN.md)

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-orange?style=flat-square&logo=pytorch)
![OpenCV](https://img.shields.io/badge/OpenCV-Latest-green?style=flat-square&logo=opencv)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=flat-square)

</div>

A Python toolkit specifically designed for seamless tile processing, featuring AI-powered background removal and intelligent element extraction. Mainly used for seamless textures, pattern materials, and other seamless tile images.

## 📋 Table of Contents

- [✨ Key Features](#-key-features)
- [🚀 Quick Start](#-quick-start)
- [🔧 Running the Project](#-running-the-project)
- [📁 Project Structure](#-project-structure)
- [📝 File Naming Convention](#-file-naming-convention)
- [🔍 Technical Features](#-technical-features)
- [🎯 Use Cases](#-use-cases)
- [📝 Notes](#-notes)

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

### 🎨 Intelligent Color Analysis
- Automatic analysis of main background colors
- Extract top 3 primary color values
- Support RGBA color format
- Output color data in JSON format

### 📍 Precise Coordinate Positioning
- Automatic recording of element coordinates in original images
- Filenames contain complete positioning information
- Supports subsequent editing and precise positioning

### 🔗 Result Merging & Visualization
- Merge color analysis and element extraction results
- Create 1536x1536 background color images
- Automatic BGR to RGB channel correction
- Support transparency preservation and precise element positioning

## 🚀 Quick Start

### Requirements
- **Required**: NVIDIA GPU (CUDA support)
- **Required**: Python 3.8+
- **Required**: NVIDIA graphics driver
- **Supported**: Windows 10/11, Linux, macOS

### 🖥️ Cross-Platform Environment Setup

#### Windows System
```powershell
# Method 1: Use PowerShell script (Recommended)
.\install-env.ps1

# Method 2: Manual installation
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
```

#### Linux System
```bash
# Method 1: Use Shell script (Recommended)
chmod +x install-env.sh
./install-env.sh

# Method 2: Manual installation
python3 -m venv venv
source venv/bin/activate
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
```

#### macOS System
```bash
# Method 1: Use Shell script (Recommended)
chmod +x install-env.sh
./install-env.sh

# Method 2: Manual installation
python3 -m venv venv
source venv/bin/activate
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
```

### 📋 Installation Script Features

**Automatic Detection:**
- ✅ Python environment detection
- ✅ NVIDIA GPU detection
- ✅ CUDA version detection
- ✅ Automatic virtual environment creation
- ✅ Smart dependency installation

**Cross-Platform Support:**
- 🪟 Windows: PowerShell script
- 🐧 Linux: Bash script
- 🍎 macOS: Bash script

**Error Handling:**
- 🚫 Automatically stops installation if no GPU detected
- 🔧 Detailed error messages and solutions
- 📝 Complete installation logs

### 🔧 Manual Dependency Installation
```bash
# After activating virtual environment
pip install -r requirements.txt
```

## 🎯 Usage

### 1. Activate Environment
```bash
# Windows
.\venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

### 2. Configuration File Setup
The project uses `config.json` configuration file to manage various parameters:

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

**Configuration Description:**
- `INPUT_PATH`: Input image path
- `OUTPUT_PATH`: Background removal result output directory
- `SAVE_BOTH`: Whether to save both transparent image and mask
- `INPUT_SIZE`: Model input size
- `RGBA_PATH`: Seamless tile transparent image path
- `MASK_PATH`: Seamless tile mask image path
- `OUTPUT_DIR`: Element extraction output directory
- `MIN_AREA`: Minimum element area threshold (pixels)

### 3. Running the Project

#### Background Removal
```bash
# Run Python script directly
python rmbg.py
```

#### Element Extraction
```bash
# Run Python script directly
python grid_split_elements.py
```

#### Color Analysis
```bash
# Run Python script directly
python color_analyzer.py --summary
```

#### Result Merging
```bash
# Run Python script directly
python merge_results_better.py

# Or use batch file (Windows)
# This feature currently only has Python script, can be run directly
```

#### Complete Pipeline
```bash
# Use shell script (Linux/macOS)
./run.sh
```

### 4. Deactivate Environment
```bash
deactivate
```

## 📁 Project Structure

```
rmbg-seamlessTile/
├── input/                    # Input images directory
├── output/                   # Output results directory
│   ├── rmbg_output/         # Background removal results
│   └── merged_output/       # Merged output results
├── config.json              # Configuration file
├── rmbg.py                 # Background removal core code
├── color_analyzer.py       # Color analysis core code
├── grid_split_elements.py  # Element extraction core code
├── merge_results_better.py # Result merging core code
├── requirements.txt         # Python dependencies
├── install-env.ps1         # Windows environment setup script
├── install-env.sh          # Linux/macOS environment setup script
├── run.sh                  # Linux/macOS pipeline script
└── *_guide.md              # Usage guide documents for each feature
```

## 🔧 Configuration

### Background Removal Config
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

## 📋 File Naming Convention

The project follows a unified naming convention to ensure consistency between Python scripts, batch files, and documentation:

### Core Feature Modules
- **Background Removal**: `rmbg.py` ←→ `rmbg_guide.md`
- **Color Analysis**: `color_analyzer.py` ←→ `color_analysis_guide.md`
- **Element Extraction**: `grid_split_elements.py` ←→ `element_extraction_guide.md`
- **Result Merging**: `merge_results_better.py` ←→ `results_merge_guide.md`
- **Pipeline Execution**: `run.sh` ←→ `run.md`

### Naming Rules
- **Python Scripts**: Use snake_case naming convention
- **Documentation**: Feature name + `_guide.md`
- All filenames use English, avoiding Chinese characters

For detailed conventions, please refer to the corresponding `*_guide.md` documents.

### Element Extraction Config
```json
{
  "4图合并提取元素": {
    "RGBA_PATH": "output/rmbg_output/rgba.png",
    "MASK_PATH": "output/rmbg_output/mask.png",
    "OUTPUT_DIR": "output/merged_output",
    "MIN_AREA": 10
  }
}
```

## 📊 Output Files

### Background Removal Output
- `原文件名_rgba.png` - Transparent background image
- `原文件名_mask.png` - Mask image

### Element Extraction Output
- `merged_rgba.png` - Merged 4K transparent image
- `merged_mask.png` - Merged 4K mask image
- `elements/` - Extracted elements folder
- `elements_output.json` - Element position information in JSON format

### Color Analysis Output
- `colors_output.json` - Main background colors in JSON format
- Contains `backgroundColor1`, `backgroundColor2`, `backgroundColor3`

### Result Merging Output
- `merged_final_better.png` - Final merged 1536x1536 image
- Combines background color with extracted elements
- Maintains transparency and correct positioning

### Element Naming Format
```
element_000.png
```
- `000` - Element index (natural number sorting)
- Position information stored in JSON format

## 🎯 Use Cases

- **Seamless Tile Processing** - Handle seamless textures and pattern materials
- **Pattern Element Extraction** - Extract complete elements from seamless patterns
- **Asset Library Management** - Batch extract and manage seamless tile elements
- **Texture Design** - Process textures that require seamless tiling

## 🔍 Technical Features

- **AI-Powered** - Uses latest RMBG-2.0 model
- **Smart Detection** - Automatic element recognition and extraction
- **Color Analysis** - Intelligent background color extraction
- **Result Merging** - Automatic BGR to RGB channel correction
- **Precise Coordinates** - Maintains accurate element positioning
- **Cross-Platform** - Supports Windows, Linux, macOS
- **Flexible Configuration** - Easy parameter adjustment via config file
- **Unified Naming** - Consistent file naming convention across all platforms

## 📝 Important Notes

- **Important**: This project requires NVIDIA GPU support and cannot run on CPU-only systems
- Input images should be seamless tiles for best results
- AI models are automatically downloaded on first run
- Recommended image resolution: 1024x1024 or higher
- Transparent and mask images must have identical dimensions

## 🚨 Troubleshooting

### Common Issues

1. **GPU Detection Failed**
   - Ensure NVIDIA graphics driver is installed
   - Confirm GPU supports CUDA computation
   - Restart system and try again

2. **Installation Failed**
   - Check network connection
   - Try using VPN or proxy
   - Manually install PyTorch GPU version

3. **CUDA Version Mismatch**
   - Use pre-compiled version (recommended)
   - Or install matching CUDA Toolkit

### System-Specific Issues

**Windows:**
- Ensure PowerShell execution policy allows script execution
- Run PowerShell as administrator

**Linux:**
- Ensure script has execution permission: `chmod +x install-env.sh`
- Use bash shell: `bash install-env.sh`

**macOS:**
- Ensure Homebrew is installed (for Python installation)
- May need to allow unsigned script execution

## 🤝 Contributing

Issues and Pull Requests are welcome!

## 📄 License

This project is licensed under the MIT License.

---

**Making seamless tile processing simpler!** 🔄✨
