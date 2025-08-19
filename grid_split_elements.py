import argparse
import os
import configparser
import numpy as np
import cv2


def load_config(config_file="config.ini"):
    """从config.ini文件加载配置"""
    config = configparser.ConfigParser()
    
    if not os.path.exists(config_file):
        print(f"警告：配置文件 {config_file} 不存在，将使用默认配置")
        return None
    
    config.read(config_file, encoding='utf-8')
    
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


def merge_4_images_2x2(image_paths, output_path):
    """将4张图片按2x2方式合并成一张大图"""
    if len(image_paths) != 4:
        raise ValueError("需要提供4张图片路径")
    
    # 读取第一张图片获取尺寸
    first_img = cv2.imread(image_paths[0], cv2.IMREAD_UNCHANGED)
    if first_img is None:
        raise ValueError(f"无法读取图片: {image_paths[0]}")
    
    h, w = first_img.shape[:2]
    channels = first_img.shape[2] if len(first_img.shape) > 2 else 1
    
    # 创建2x2合并后的大图
    merged_height = h * 2
    merged_width = w * 2
    
    if channels == 4:  # RGBA
        merged_img = np.zeros((merged_height, merged_width, 4), dtype=np.uint8)
    elif channels == 3:  # RGB
        merged_img = np.zeros((merged_height, merged_width, 3), dtype=np.uint8)
    else:  # Grayscale
        merged_img = np.zeros((merged_height, merged_width), dtype=np.uint8)
    
    # 按2x2方式合并图片
    positions = [
        (0, 0),      # 左上
        (0, w),      # 右上
        (h, 0),      # 左下
        (h, w)       # 右下
    ]
    
    for i, (img_path, (y_start, x_start)) in enumerate(zip(image_paths, positions)):
        img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
        if img is None:
            raise ValueError(f"无法读取图片: {img_path}")
        
        # 确保尺寸一致
        if img.shape[:2] != (h, w):
            raise ValueError(f"图片尺寸不一致: {img_path}")
        
        # 将图片放置到对应位置
        merged_img[y_start:y_start+h, x_start:x_start+w] = img
    
    # 保存合并后的图片
    cv2.imwrite(output_path, merged_img)
    print(f"4张图片已合并为: {output_path}")
    print(f"合并后尺寸: {merged_width}x{merged_height}")
    
    return merged_img


def extract_elements_from_merged_image(rgba_path, mask_path, original_size, min_area=100):
    """从合并后的大图中提取独立元素，并转换坐标到原图"""
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
    orig_h, orig_w = original_size
    
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
        
        # 将合并图坐标转换为原图坐标
        # 合并图是2x2排列，原图在左上角
        orig_x = x % orig_w
        orig_y = y % orig_h
        
        # 处理跨边界的元素
        # 如果元素跨越了原图边界，需要计算在原图中的实际位置
        orig_x1 = orig_x
        orig_y1 = orig_y
        orig_x2 = orig_x1 + w
        orig_y2 = orig_y1 + h
        
        # 如果超出原图边界，进行裁剪以获得在原图范围内的坐标
        if orig_x2 > orig_w:
            orig_x2 = orig_w
        if orig_y2 > orig_h:
            orig_y2 = orig_h
            
        # 确保坐标有效
        if orig_x2 <= orig_x1 or orig_y2 <= orig_y1:
            continue
            
        # 原图坐标信息：(x1, y1, x2, y2) 和合并图坐标信息
        coords_info = {
            'merged_coords': (x, y, x + w, y + h),  # 合并图中的坐标
            'original_coords': (orig_x1, orig_y1, orig_x2, orig_y2),  # 原图中的坐标
            'size': (w, h)  # 元素尺寸
        }
        
        elements.append((element_rgba, coords_info))
    
    return elements


def process_4_images_merge(rgba_paths, mask_paths, output_dir, min_area=100):
    """处理4张透明图片和4张蒙版图片，合并后提取元素"""
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取原图尺寸（读取第一张图片）
    first_img = cv2.imread(rgba_paths[0], cv2.IMREAD_UNCHANGED)
    if first_img is None:
        raise ValueError(f"无法读取图片: {rgba_paths[0]}")
    original_size = first_img.shape[:2]  # (height, width)
    
    # 合并4张透明图片
    merged_rgba_path = os.path.join(output_dir, "merged_rgba.png")
    merged_rgba = merge_4_images_2x2(rgba_paths, merged_rgba_path)
    
    # 合并4张蒙版图片
    merged_mask_path = os.path.join(output_dir, "merged_mask.png")
    merged_mask = merge_4_images_2x2(mask_paths, merged_mask_path)
    
    # 从合并后的大图中提取元素
    print("正在从合并后的大图中提取元素...")
    all_elements = extract_elements_from_merged_image(merged_rgba_path, merged_mask_path, original_size, min_area)
    
    # 保存提取的元素
    elements_dir = os.path.join(output_dir, "elements")
    os.makedirs(elements_dir, exist_ok=True)
    
    for idx, (element_img, coords_info) in enumerate(all_elements):
        # 使用原图坐标作为文件名
        orig_coords = coords_info['original_coords']
        orig_x1, orig_y1, orig_x2, orig_y2 = orig_coords
        w, h = coords_info['size']
        
        # 使用原图坐标信息作为文件名
        filename = f"element_{idx:03d}_orig_x{orig_x1}_y{orig_y1}_w{orig_x2-orig_x1}_h{orig_y2-orig_y1}.png"
        filepath = os.path.join(elements_dir, filename)
        cv2.imwrite(filepath, element_img)
        print(f"保存元素: {filename}")
    
    # 创建元素位置信息文件
    info_file = os.path.join(output_dir, "elements_info.txt")
    with open(info_file, 'w', encoding='utf-8') as f:
        f.write("元素索引\t文件名\t原图X坐标\t原图Y坐标\t原图宽度\t原图高度\t合并图X坐标\t合并图Y坐标\t合并图宽度\t合并图高度\n")
        for idx, (_, coords_info) in enumerate(all_elements):
            orig_coords = coords_info['original_coords']
            merged_coords = coords_info['merged_coords']
            orig_x1, orig_y1, orig_x2, orig_y2 = orig_coords
            merged_x1, merged_y1, merged_x2, merged_y2 = merged_coords
            
            filename = f"element_{idx:03d}_orig_x{orig_x1}_y{orig_y1}_w{orig_x2-orig_x1}_h{orig_y2-orig_y1}.png"
            f.write(f"{idx}\t{filename}\t{orig_x1}\t{orig_y1}\t{orig_x2-orig_x1}\t{orig_y2-orig_y1}\t{merged_x1}\t{merged_y1}\t{merged_x2-merged_x1}\t{merged_y2-merged_y1}\n")
    
    print(f"\n处理完成！共提取 {len(all_elements)} 个元素")
    print(f"元素保存在: {elements_dir}")
    print(f"位置信息保存在: {info_file}")
    print(f"合并后的透明图: {merged_rgba_path}")
    print(f"合并后的蒙版图: {merged_mask_path}")
    print(f"原图尺寸: {original_size[1]}x{original_size[0]} (宽x高)")
    print(f"元素文件名现在使用原图坐标命名")


def main():
    parser = argparse.ArgumentParser(description="将4张无缝四方连续图片合并后提取元素")
    parser.add_argument("--rgba-paths", nargs=4, required=False, 
                       help="4张透明图片路径，顺序：左上、右上、左下、右下")
    parser.add_argument("--mask-paths", nargs=4, required=False,
                       help="4张蒙版图片路径，顺序：左上、右上、左下、右下")
    parser.add_argument("--output", default=None, help="输出目录")
    parser.add_argument("--min-area", type=int, default=None, help="最小元素面积阈值")
    parser.add_argument("--config", default="config.ini", help="配置文件路径")
    
    args = parser.parse_args()
    
    # 加载配置文件
    config = load_config(args.config)
    
    # 从配置文件或命令行参数获取值
    if args.rgba_paths:
        rgba_paths = args.rgba_paths
    else:
        # 从配置文件读取单张图片路径，然后复制4次
        rgba_path = get_config_value(config, '4图合并提取元素', 'RGBA_PATH', '')
        if not rgba_path:
            print("错误：配置文件中未找到 RGBA_PATH，请设置或使用命令行参数")
            return
        
        # 复制4次路径
        rgba_paths = [rgba_path] * 4
        print(f"从配置文件读取透明图片路径: {rgba_path}")
        print("将自动复制4次进行合并")
    
    if args.mask_paths:
        mask_paths = args.mask_paths
    else:
        # 从配置文件读取单张蒙版图片路径，然后复制4次
        mask_path = get_config_value(config, '4图合并提取元素', 'MASK_PATH', '')
        if not mask_path:
            print("错误：配置文件中未找到 MASK_PATH，请设置或使用命令行参数")
            return
        
        # 复制4次路径
        mask_paths = [mask_path] * 4
        print(f"从配置文件读取蒙版图片路径: {mask_path}")
        print("将自动复制4次进行合并")
    
    # 获取输出目录和最小面积阈值
    output_dir = args.output or get_config_value(config, '4图合并提取元素', 'OUTPUT_DIR', 'merged_output')
    min_area = args.min_area or int(get_config_value(config, '4图合并提取元素', 'MIN_AREA', '100'))
    
    print(f"输出目录: {output_dir}")
    print(f"最小面积阈值: {min_area}")
    
    # 处理4张图片合并
    process_4_images_merge(
        rgba_paths, 
        mask_paths, 
        output_dir, 
        min_area
    )


if __name__ == "__main__":
    main()
