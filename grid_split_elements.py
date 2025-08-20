import argparse
import os
import json
import base64
import io
import numpy as np
import cv2
from PIL import Image


def load_config(config_file="config.json"):
    """从config.json文件加载配置"""
    if not os.path.exists(config_file):
        print(f"警告：配置文件 {config_file} 不存在，将使用默认配置")
        return None
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        print(f"读取配置文件失败: {e}")
        return None
    
    # 检查是否有4图合并提取元素配置节
    if '4图合并提取元素' not in config:
        print("警告：配置文件中没有 [4图合并提取元素] 节，将使用默认配置")
        return None
    
    return config


def get_config_value(config, section, key, default_value):
    """从配置中获取值，如果不存在则返回默认值"""
    if config and section in config and key in config[section]:
        return config[section][key]
    return default_value


def image_to_base64(image_array):
    """将numpy数组转换为base64编码的PNG图片"""
    try:
        # 确保图片是uint8类型
        if image_array.dtype != np.uint8:
            image_array = image_array.astype(np.uint8)
        
        # 转换为PIL Image
        if len(image_array.shape) == 3:
            pil_image = Image.fromarray(image_array)
        else:
            pil_image = Image.fromarray(image_array, mode='L')
        
        # 转换为base64
        buffer = io.BytesIO()
        pil_image.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"
    except Exception as e:
        print(f"转换图片为base64失败: {e}")
        return ""


def generate_json_output(all_elements, output_file="elements_output.json"):
    """生成包含mask和bbox的JSON输出"""
    try:
        result = {
            "masks": []
        }
        
        for element_img, coords_info in all_elements:
            # 转换图片为base64
            mask_base64 = image_to_base64(element_img)
            
            # 获取bbox坐标
            coords = coords_info['coords']
            x1, y1, x2, y2 = coords
            
            # 创建bbox坐标点（顺时针顺序：左上、右上、右下、左下）
            bbox = [
                f"{x1},{y1}",  # 左上
                f"{x2},{y1}",  # 右上
                f"{x2},{y2}",  # 右下
                f"{x1},{y2}"   # 左下
            ]
            
            mask_info = {
                "mask": mask_base64,
                "bbox": bbox
            }
            
            result["masks"].append(mask_info)
        
        # 保存JSON文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"JSON输出已保存到: {output_file}")
        return result
        
    except Exception as e:
        print(f"生成JSON输出失败: {e}")
        return None


def extract_elements_from_image(rgba_path, mask_path, min_area=100):
    """从单张图片中提取独立元素"""
    # 读取图片
    rgba_img = cv2.imread(rgba_path, cv2.IMREAD_UNCHANGED)
    mask_img = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    
    if rgba_img is None or mask_img is None:
        raise ValueError("无法读取输入图片")
    
    # 确保尺寸一致
    if rgba_img.shape[:2] != mask_img.shape[:2]:
        raise ValueError("透明图片和蒙版图片尺寸不一致")
    
    # 二值化mask
    _, binary_mask = cv2.threshold(mask_img, 127, 255, cv2.THRESH_BINARY)
    
    # 查找连通区域
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_mask, connectivity=8)
    
    elements = []
    img_h, img_w = rgba_img.shape[:2]
    
    for i in range(1, num_labels):  # 跳过背景(label=0)
        # 获取当前元素的统计信息
        x, y, w, h, area = stats[i]
        
        # 过滤太小的区域
        if area < min_area:
            continue
        
        # 创建当前元素的mask
        element_mask = (labels == i).astype(np.uint8) * 255
        
        # 提取元素区域
        element_rgba = rgba_img[y:y+h, x:x+w].copy()
        element_mask_crop = element_mask[y:y+h, x:x+w]
        
        # 应用mask到alpha通道
        if element_rgba.shape[2] == 4:
            element_rgba[:, :, 3] = element_mask_crop
        else:
            # 如果不是RGBA，转换为RGBA
            element_rgba = cv2.cvtColor(element_rgba, cv2.COLOR_RGB2RGBA)
            element_rgba[:, :, 3] = element_mask_crop
        
        # 坐标信息：直接使用图片中的坐标
        coords_info = {
            'coords': (x, y, x + w, y + h),  # 图片中的坐标
            'size': (w, h)  # 元素尺寸
        }
        
        elements.append((element_rgba, coords_info))
    
    return elements


def process_single_image(rgba_path, mask_path, output_dir, min_area=100):
    """处理单张图片，提取元素"""
    # 清空输出目录（如果存在）
    if os.path.exists(output_dir):
        import shutil
        shutil.rmtree(output_dir)
        print(f"已清空输出目录: {output_dir}")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 从图片中提取元素
    print("正在从图片中提取元素...")
    all_elements = extract_elements_from_image(rgba_path, mask_path, min_area)
    
    # 获取图片尺寸
    rgba_img = cv2.imread(rgba_path, cv2.IMREAD_UNCHANGED)
    if rgba_img is not None:
        img_h, img_w = rgba_img.shape[:2]
    else:
        img_w, img_h = 0, 0
    
    # 保存提取的元素
    elements_dir = os.path.join(output_dir, "elements")
    os.makedirs(elements_dir, exist_ok=True)
    
    for idx, (element_img, coords_info) in enumerate(all_elements):
        # 使用简单的自然数排序命名
        filename = f"element_{idx:03d}.png"
        filepath = os.path.join(elements_dir, filename)
        cv2.imwrite(filepath, element_img)
        print(f"保存元素: {filename}")
    
    print(f"\n处理完成！共提取 {len(all_elements)} 个元素")
    print(f"元素保存在: {elements_dir}")
    print(f"原图尺寸: {img_w}x{img_h} (宽x高)")
    
    # 生成JSON输出
    json_output_file = os.path.join(output_dir, "elements_output.json")
    generate_json_output(all_elements, json_output_file)


def main():
    parser = argparse.ArgumentParser(description="从单张图片中提取独立元素")
    parser.add_argument("--rgba-path", required=False, 
                       help="透明图片路径")
    parser.add_argument("--mask-path", required=False,
                       help="蒙版图片路径")
    parser.add_argument("--output", default=None, help="输出目录")
    parser.add_argument("--min-area", type=int, default=None, help="最小元素面积阈值")
    parser.add_argument("--config", default="config.json", help="配置文件路径")
    
    args = parser.parse_args()
    
    # 加载配置文件
    config = load_config(args.config)
    
    # 从配置文件或命令行参数获取值
    if args.rgba_path:
        rgba_path = args.rgba_path
    else:
        rgba_path = get_config_value(config, '4图合并提取元素', 'RGBA_PATH', '')
        if not rgba_path:
            print("错误：配置文件中未找到 RGBA_PATH，请设置或使用命令行参数")
            return
        print(f"从配置文件读取透明图片路径: {rgba_path}")
    
    if args.mask_path:
        mask_path = args.mask_path
    else:
        mask_path = get_config_value(config, '4图合并提取元素', 'MASK_PATH', '')
        if not mask_path:
            print("错误：配置文件中未找到 MASK_PATH，请设置或使用命令行参数")
            return
        print(f"从配置文件读取蒙版图片路径: {mask_path}")
    
    # 获取输出目录和最小面积阈值
    output_dir = args.output or get_config_value(config, '4图合并提取元素', 'OUTPUT_DIR', 'merged_output')
    min_area = args.min_area or int(get_config_value(config, '4图合并提取元素', 'MIN_AREA', '100'))
    
    print(f"输出目录: {output_dir}")
    print(f"最小面积阈值: {min_area}")
    
    # 处理单张图片
    process_single_image(rgba_path, mask_path, output_dir, min_area)


if __name__ == "__main__":
    main()
