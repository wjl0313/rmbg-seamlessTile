#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
颜色分析脚本
分析config.json中设置的图片路径，获取占比最大的三个颜色并返回rgba色值
"""

import json
import os
import re
from PIL import Image
import numpy as np
from collections import Counter
from typing import List, Tuple, Optional, Dict
import argparse


class ColorAnalyzer:
    """颜色分析器"""
    
    def __init__(self, config_file: str = "config.json"):
        """
        初始化颜色分析器
        
        Args:
            config_file: 配置文件路径
        """
        self.config_file = config_file
        self.config = None
        self.load_config()
    
    def load_config(self) -> bool:
        """
        加载配置文件
        
        Returns:
            是否成功加载配置
        """
        try:
            if not os.path.exists(self.config_file):
                print(f"警告：配置文件 {self.config_file} 不存在")
                return False
            
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            return True
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return False
    
    def get_image_paths_from_config(self) -> List[str]:
        """
        从配置文件中获取图片路径
        
        Returns:
            图片路径列表
        """
        image_paths = []
        
        if not self.config:
            print("配置文件未加载")
            return image_paths
        
        # 只检查[图片去背景]节的INPUT_PATH
        if '图片去背景' in self.config:
            input_path = self.config['图片去背景'].get('INPUT_PATH', '')
            if input_path and self._is_image_file(input_path):
                if os.path.exists(input_path):
                    image_paths.append(input_path)
                    print(f"使用[图片去背景]的INPUT_PATH: {input_path}")
                else:
                    print(f"警告：[图片去背景]的INPUT_PATH不存在: {input_path}")
        
        return image_paths
    
    def _is_image_file(self, path: str) -> bool:
        """
        检查路径是否是图片文件
        
        Args:
            path: 文件路径
            
        Returns:
            是否是图片文件
        """
        if not path or not isinstance(path, str):
            return False
        
        # 常见的图片文件扩展名
        image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp'}
        _, ext = os.path.splitext(path.lower())
        return ext in image_extensions
    
    def analyze_image_colors(self, image_path: str) -> Dict[str, str]:
        """
        分析图片的主要颜色，返回占比最大的3个颜色，按占比排序
        
        Args:
            image_path: 图片路径
            
        Returns:
            颜色字典，key为backgroundColor1/2/3，value为rgba格式色值
        """
        try:
            # 打开图片
            with Image.open(image_path) as img:
                # 转换为RGB模式
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # 获取图片尺寸
                width, height = img.size
                
                # 将图片转换为numpy数组
                img_array = np.array(img)
                
                # 重塑为二维数组，每行代表一个像素的RGB值
                pixels = img_array.reshape(-1, 3)
                
                # 统计颜色出现次数
                color_counts = Counter(map(tuple, pixels))
                
                # 获取占比最大的颜色，但需要确保颜色有足够区分度
                total_pixels = len(pixels)
                all_colors = color_counts.most_common()
                
                # 选择有足够区分度的颜色
                selected_colors = []
                min_distance = 30  # 最小颜色距离阈值
                
                for color, count in all_colors:
                    if len(selected_colors) >= 3:
                        break
                    
                    # 检查与已选颜色的距离
                    is_different = True
                    for selected_color in selected_colors:
                        distance = self._color_distance(color, selected_color)
                        if distance < min_distance:
                            is_different = False
                            break
                    
                    if is_different:
                        selected_colors.append(color)
                
                # 如果没找到足够的颜色，降低阈值
                if len(selected_colors) < 3:
                    min_distance = 15
                    for color, count in all_colors:
                        if len(selected_colors) >= 3:
                            break
                        
                        is_different = True
                        for selected_color in selected_colors:
                            distance = self._color_distance(color, selected_color)
                            if distance < min_distance:
                                is_different = False
                                break
                        
                        if is_different:
                            selected_colors.append(color)
                
                # 构建结果字典
                result = {}
                for i, color in enumerate(selected_colors[:3]):
                    r, g, b = color
                    rgba_color = f"rgba({r}, {g}, {b}, 1.0)"
                    
                    if i == 0:
                        result['backgroundColor1'] = rgba_color
                    elif i == 1:
                        result['backgroundColor2'] = rgba_color
                    elif i == 2:
                        result['backgroundColor3'] = rgba_color
                
                return result
                
        except Exception as e:
            print(f"分析图片 {image_path} 失败: {e}")
            return {}
    
    def _color_distance(self, color1: Tuple[int, int, int], color2: Tuple[int, int, int]) -> float:
        """
        计算两个颜色之间的欧几里得距离
        
        Args:
            color1: 第一个颜色 (R, G, B)
            color2: 第二个颜色 (R, G, B)
            
        Returns:
            颜色距离
        """
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        
        # 使用更安全的计算方式避免溢出
        r_diff = float(r1) - float(r2)
        g_diff = float(g1) - float(g2)
        b_diff = float(b1) - float(b2)
        
        distance = (r_diff * r_diff + g_diff * g_diff + b_diff * b_diff) ** 0.5
        return distance
    
    def analyze_all_images(self) -> dict:
        """
        分析配置文件中所有图片的颜色，每张图片返回3个主要颜色
        
        Returns:
            分析结果字典，key为图片路径，value为颜色字典
        """
        image_paths = self.get_image_paths_from_config()
        
        if not image_paths:
            print("未找到有效的图片路径")
            return {}
        
        results = {}
        
        for image_path in image_paths:
            print(f"正在分析图片: {image_path}")
            colors = self.analyze_image_colors(image_path)
            
            if colors:
                results[image_path] = colors
                print(f"  主要颜色:")
                for key, rgba_color in colors.items():
                    print(f"    {key}: {rgba_color}")
            else:
                print(f"  分析失败")
        
        return results
    
    def get_dominant_colors_summary(self) -> Dict[str, str]:
        """
        获取所有图片的综合主要颜色，返回前3个，按占比排序
        
        Returns:
            综合主要颜色字典，key为backgroundColor1/2/3，value为rgba格式色值
        """
        all_results = self.analyze_all_images()
        
        if not all_results:
            return {}
        
        # 收集所有颜色及其权重
        color_weights = {}
        
        for image_path, colors in all_results.items():
            for key, rgba_color in colors.items():
                if rgba_color in color_weights:
                    color_weights[rgba_color] += 1  # 简单计数，每张图片权重相等
                else:
                    color_weights[rgba_color] = 1
        
        # 按权重排序，获取前3个颜色
        sorted_colors = sorted(color_weights.items(), key=lambda x: x[1], reverse=True)
        
        # 构建结果字典
        result = {}
        for i, (rgba_color, weight) in enumerate(sorted_colors[:3]):
            if i == 0:
                result['backgroundColor1'] = rgba_color
            elif i == 1:
                result['backgroundColor2'] = rgba_color
            elif i == 2:
                result['backgroundColor3'] = rgba_color
        
        return result

    def save_colors_to_json(self, output_file: str = "output/merged_output/colors_output.json") -> bool:
        """
        将颜色分析结果保存为JSON文件
        """
        try:
            colors = self.get_dominant_colors_summary()
            if not colors:
                print("无颜色数据可保存")
                return False
            
            # 确保输出目录存在
            output_dir = os.path.dirname(output_file)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                print(f"创建输出目录: {output_dir}")
            
            # 转换rgba字符串为数组格式，保持alpha值为0.0-1.0范围
            colors_array = {}
            for key, rgba_str in colors.items():
                # 解析rgba(r, g, b, a)为[r, g, b, a]
                match = re.search(r'rgba\((\d+),\s*(\d+),\s*(\d+),\s*([\d.]+)\)', rgba_str)
                if match:
                    r, g, b, a = int(match.group(1)), int(match.group(2)), int(match.group(3)), float(match.group(4))
                    # 保持alpha值为0.0-1.0范围
                    colors_array[key] = [r, g, b, a]
                else:
                    colors_array[key] = [0, 0, 0, 0]  # 默认值
            
            # 确保所有三个背景颜色字段都存在
            if 'backgroundColor1' not in colors_array:
                colors_array['backgroundColor1'] = [0, 0, 0, 0]
            if 'backgroundColor2' not in colors_array:
                colors_array['backgroundColor2'] = [0, 0, 0, 0]
            if 'backgroundColor3' not in colors_array:
                colors_array['backgroundColor3'] = [0, 0, 0, 0]
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(colors_array, f, indent=2, ensure_ascii=False)
            
            print(f"颜色数据已保存到: {output_file}")
            return True
            
        except Exception as e:
            print(f"保存颜色JSON失败: {e}")
            return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='分析config.json中图片的主要颜色，返回占比最大的3个rgba色值')
    parser.add_argument('--config', '-c', default='config.json', help='配置文件路径')
    parser.add_argument('--summary', '-s', action='store_true', help='显示综合主要颜色')
    parser.add_argument('--json', '-j', help='保存颜色结果为JSON文件')
    
    args = parser.parse_args()
    
    # 创建颜色分析器
    analyzer = ColorAnalyzer(args.config)
    
    if args.json:
        # 保存为JSON文件
        success = analyzer.save_colors_to_json(args.json)
        if not success:
            print("JSON文件保存失败")
    elif args.summary:
        # 显示综合主要颜色并自动保存到merged_output目录
        print("=" * 50)
        print("综合主要颜色分析")
        print("=" * 50)
        
        dominant_colors = analyzer.get_dominant_colors_summary()
        
        if dominant_colors:
            print(f"\n前3个主要颜色:")
            for key, rgba_color in dominant_colors.items():
                print(f"{key}: {rgba_color}")
            
            # 自动保存到merged_output目录
            print("\n自动保存颜色结果到merged_output目录...")
            success = analyzer.save_colors_to_json("output/merged_output/colors_output.json")
            if success:
                print("✓ 颜色结果已保存到 output/merged_output/colors_output.json")
            else:
                print("✗ 颜色结果保存失败")
        else:
            print("未找到有效的颜色数据")
    else:
        # 显示每张图片的详细分析
        print("=" * 50)
        print("图片颜色详细分析")
        print("=" * 50)
        
        results = analyzer.analyze_all_images()
        
        if results:
            print(f"\n共分析了 {len(results)} 张图片")
        else:
            print("未找到有效的图片路径")


if __name__ == "__main__":
    main()
