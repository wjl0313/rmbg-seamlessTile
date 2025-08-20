# 图片去背景配置说明

## 配置文件说明

所有运行参数都集中在 `config.ini` 文件中，修改此文件即可配置运行参数：

```ini
[图片去背景]
# 输入图片路径
INPUT_PATH=input/test.png
# 输出文件夹路径
OUTPUT_PATH=output/rmbg_output
# 是否同时输出掩码和透明图
SAVE_BOTH=true
# 模型输入尺寸
INPUT_SIZE=1024

[4图合并提取元素]
# 四方连续透明图片路径
RGBA_PATH=output/rmbg_output/rgba.png
# 四方连续蒙版图片路径
MASK_PATH=output/rmbg_output/mask.png
# 输出目录
OUTPUT_DIR=output/merged_output
# 最小元素面积阈值（像素）
MIN_AREA=10
```

## 路径配置说明

### 相对路径的优势
- **跨平台兼容**：Windows、Linux、macOS 都可以使用
- **项目可移植**：整个项目文件夹可以移动到任何位置
- **团队协作友好**：不同用户的路径结构可以保持一致

### 路径格式
- **Windows**: 可以使用 `\` 或 `/` 作为分隔符
- **Linux/macOS**: 使用 `/` 作为分隔符
- **推荐**: 统一使用 `/` 作为分隔符，确保跨平台兼容

### 路径示例
```
# 相对于项目根目录的路径
input/test.png                    # 项目根目录下的 input 文件夹
output/rmbg_output               # 项目根目录下的 output/rmbg_output 文件夹
../other_folder/image.png        # 上级目录中的文件
./current_folder/file.png        # 当前目录中的文件
```

## 参数说明

### 图片去背景参数
| 参数 | 说明 | 示例值 |
|------|------|--------|
| `INPUT_PATH` | 输入图片路径（相对路径） | `input/test.png` |
| `OUTPUT_PATH` | 输出文件夹路径（相对路径） | `output/rmbg_output` |
| `SAVE_BOTH` | 是否同时保存掩码和透明图 | `true` 或 `false` |
| `INPUT_SIZE` | 模型输入尺寸 | `1024` |

### 4图合并提取元素参数
| 参数 | 说明 | 示例值 |
|------|------|--------|
| `RGBA_PATH` | 四方连续透明图片路径（相对路径） | `output/rmbg_output/rgba.png` |
| `MASK_PATH` | 四方连续蒙版图片路径（相对路径） | `output/rmbg_output/mask.png` |
| `OUTPUT_DIR` | 输出目录（相对路径） | `output/merged_output` |
| `MIN_AREA` | 最小元素面积阈值 | `10` |

## 使用方法

1. 修改 `config.ini` 中的参数
2. 运行对应的批处理文件：
   - `图片去背景.bat`: 处理单张图片
   - `4图合并提取元素.bat`: 合并图片并提取元素

## 输出文件说明

- **掩码文件**: `原文件名_mask.png`
- **透明背景文件**: `原文件名_rgba.png`

## 注意事项

1. **路径格式**：建议使用 `/` 作为路径分隔符，确保跨平台兼容
2. **相对路径**：所有路径都相对于项目根目录（包含 config.ini 的目录）
3. **首次运行**：会自动下载官方模型到 `models` 文件夹
4. **目录创建**：输出文件夹不存在会自动创建
5. **授权设置**：需要先运行 `登录配置.bat` 完成授权设置

## 常见问题

**Q: 如何修改处理参数？**
A: 直接编辑 `config.ini` 文件，修改对应的参数值。

**Q: 如何在不同模式间切换？**
A: 修改 `config.ini` 中的 `SAVE_BOTH` 参数：
- `true`: 同时输出掩码和透明图
- `false`: 只输出透明图

**Q: 如何提高处理速度？**
A: 可以尝试减小 `INPUT_SIZE` 的值，但可能会影响输出质量。

**Q: 路径中的反斜杠和正斜杠有什么区别？**
A: 在Windows上两者都可以使用，但建议统一使用正斜杠 `/` 以确保跨平台兼容性。