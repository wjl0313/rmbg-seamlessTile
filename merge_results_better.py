#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更好的合并结果脚本
强制修复BGR到RGB通道问题
"""

import json
import base64
import io
import numpy as np
from PIL import Image
import os


def load_colors_from_json(colors_file="output/merged_output/colors_output.json"):
    """从colors_output.json加载背景颜色"""
    try:
        with open(colors_file, 'r', encoding='utf-8') as f:
            colors_data = json.load(f)
        
        # 获取backgroundColor1的颜色值
        bg1 = colors_data.get('backgroundColor1', [0, 0, 0, 1.0])
        return bg1
    except Exception as e:
        print(f"加载颜色文件失败: {e}")
        return [0, 0, 0, 1.0]


def load_elements_from_json(elements_file="output/merged_output/elements_output.json"):
    """从elements_output.json加载元素信息"""
    try:
        with open(elements_file, 'r', encoding='utf-8') as f:
            elements_data = json.load(f)
        
        return elements_data.get('masks', [])
    except Exception as e:
        print(f"加载元素文件失败: {e}")
        return []


def base64_to_image_fixed(base64_str):
    """强制修复BGR到RGB通道问题"""
    try:
        # 移除data:image/png;base64,前缀
        if 'base64,' in base64_str:
            base64_str = base64_str.split('base64,')[1]
        
        # 解码base64
        image_data = base64.b64decode(base64_str)
        
        # 转换为PIL Image
        image = Image.open(io.BytesIO(image_data))
        
        # 确保图片是RGBA模式
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        # 强制修复：交换R和B通道
        img_array = np.array(image)
        if img_array.size > 0 and len(img_array.shape) == 3:
            # 交换R和B通道
            img_array[:, :, [0, 2]] = img_array[:, :, [2, 0]]
            # 重新创建PIL图片
            image = Image.fromarray(img_array, 'RGBA')
        
        return image
    except Exception as e:
        print(f"转换base64失败: {e}")
        return None


def parse_bbox_coordinates(bbox):
    """解析bbox坐标，返回左上角和右下角坐标"""
    try:
        # bbox格式: ["x1,y1", "x2,y1", "x2,y2", "x1,y2"]
        # 我们只需要左上角(x1,y1)和右下角(x2,y2)
        top_left = bbox[0].split(',')
        bottom_right = bbox[2].split(',')
        
        x1, y1 = int(top_left[0]), int(top_left[1])
        x2, y2 = int(bottom_right[0]), int(bottom_right[1])
        
        return x1, y1, x2, y2
    except Exception as e:
        print(f"解析bbox坐标失败: {e}")
        return 0, 0, 0, 0


def create_merged_image(width=1536, height=1536):
    """创建合并后的图片"""
    print("开始创建合并图片（强制修复版本）...")
    
    # 1. 加载背景颜色
    bg_color = load_colors_from_json()
    print(f"背景颜色: {bg_color}")
    
    # 2. 创建背景图片
    # 将alpha值从0.0-1.0转换为0-255
    r, g, b, a = bg_color
    alpha = int(a * 255) if isinstance(a, float) else a
    
    # 创建RGBA图片
    background = Image.new('RGBA', (width, height), (r, g, b, alpha))
    print(f"创建背景图片: {width}x{height}, 颜色: RGBA({r},{g},{b},{alpha})")
    
    # 3. 加载元素信息
    elements = load_elements_from_json()
    print(f"加载到 {len(elements)} 个元素")
    
    # 4. 将元素贴到背景上
    for i, element_info in enumerate(elements):
        try:
            # 获取mask和bbox
            mask_base64 = element_info.get('mask', '')
            bbox = element_info.get('bbox', [])
            
            if not mask_base64 or not bbox:
                print(f"元素 {i} 缺少必要信息，跳过")
                continue
            
            # 转换base64为图片（强制修复版本）
            element_img = base64_to_image_fixed(mask_base64)
            if element_img is None:
                print(f"元素 {i} base64转换失败，跳过")
                continue
            
            # 解析坐标
            x1, y1, x2, y2 = parse_bbox_coordinates(bbox)
            
            # 确保坐标在图片范围内
            if x1 < 0 or y1 < 0 or x2 > width or y2 > height:
                print(f"元素 {i} 坐标超出范围，跳过: ({x1},{y1})-({x2},{y2})")
                continue
            
            # 调整元素图片大小以匹配bbox
            element_width = x2 - x1
            element_height = y2 - y1
            
            if element_width > 0 and element_height > 0:
                # 调整元素图片大小
                element_img_resized = element_img.resize((element_width, element_height), Image.Resampling.LANCZOS)
                
                # 将元素贴到背景上，使用alpha通道作为mask
                background.paste(element_img_resized, (x1, y1), element_img_resized)
                print(f"贴入元素 {i}: 位置({x1},{y1}), 尺寸({element_width}x{element_height})")
            else:
                print(f"元素 {i} 尺寸无效: {element_width}x{element_height}")
                
        except Exception as e:
            print(f"处理元素 {i} 时出错: {e}")
            continue
    
    # 5. 保存结果
    output_path = "output/merged_final_better.png"
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 保存为PNG格式（保持透明度）
    background.save(output_path, 'PNG')
    print(f"合并图片已保存到: {output_path}")
    
    return output_path


def main():
    """主函数"""
    print("=" * 60)
    print("更好的图片结果合并脚本")
    print("强制修复BGR到RGB通道问题")
    print("=" * 60)
    
    try:
        # 检查输入文件是否存在
        colors_file = "output/merged_output/colors_output.json"
        elements_file = "output/merged_output/elements_output.json"
        
        if not os.path.exists(colors_file):
            print(f"错误: 颜色文件不存在: {colors_file}")
            return
        
        if not os.path.exists(elements_file):
            print(f"错误: 元素文件不存在: {elements_file}")
            return
        
        print(f"✓ 颜色文件: {colors_file}")
        print(f"✓ 元素文件: {elements_file}")
        
        # 创建合并图片
        output_path = create_merged_image()
        
        if output_path and os.path.exists(output_path):
            print("\n" + "=" * 60)
            print("合并完成！")
            print(f"输出文件: {output_path}")
            print("=" * 60)
        else:
            print("\n合并失败！")
            
    except Exception as e:
        print(f"脚本执行失败: {e}")


if __name__ == "__main__":
    main()
