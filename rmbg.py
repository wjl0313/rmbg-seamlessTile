import argparse
import os
import json
from pathlib import Path
from typing import Tuple, Optional, List

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
from PIL import Image

try:
    from transformers import AutoModelForImageSegmentation
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("[警告] transformers 库未安装，将无法使用官方 RMBG-2.0 模型")


def preprocess_image(image: Image.Image, model_input_size: Tuple[int, int]) -> torch.Tensor:
	"""将 PIL.Image 预处理为模型输入 Tensor。

	Args:
		image: 输入图像（PIL.Image）。
		model_input_size: (height, width)

	Returns:
		形状为 (1, 3, H, W) 的张量。
	"""
	if image.mode != 'RGB':
		image = image.convert('RGB')

	transform = transforms.Compose([
		transforms.Resize(model_input_size),
		transforms.ToTensor(),
		transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
	])

	input_tensor = transform(image).unsqueeze(0)
	return input_tensor


def resize_mask_to_original(pred: torch.Tensor, original_size: Tuple[int, int]) -> np.ndarray:
	"""将模型输出的 (1, 1, h, w) 预测缩放回原图大小并转为 [0, 255] uint8。

	Args:
		pred: 模型输出，形状 (1, 1, h, w)，范围 [0,1]。
		original_size: (height, width)

	Returns:
		uint8 掩码，形状 (H, W)，范围 [0, 255]。
	"""
	resized = F.interpolate(pred, size=original_size, mode='bilinear', align_corners=False)
	mask = resized.squeeze().detach().cpu().numpy()
	mask = np.clip(mask * 255.0, 0, 255).astype(np.uint8)
	return mask


class BriaRMBG(nn.Module):
	def __init__(self):
		super(BriaRMBG, self).__init__()

		# 编码器
		self.enc_conv1 = nn.Conv2d(3, 32, 3, padding=1)
		self.enc_conv2 = nn.Conv2d(32, 64, 3, padding=1)
		self.enc_conv3 = nn.Conv2d(64, 128, 3, padding=1)
		self.enc_conv4 = nn.Conv2d(128, 256, 3, padding=1)

		# 解码器
		self.dec_conv1 = nn.Conv2d(256, 128, 3, padding=1)
		self.dec_conv2 = nn.Conv2d(128, 64, 3, padding=1)
		self.dec_conv3 = nn.Conv2d(64, 32, 3, padding=1)
		self.dec_conv4 = nn.Conv2d(32, 1, 3, padding=1)

		self.pool = nn.MaxPool2d(2, 2)
		self.up = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)

	def forward(self, x: torch.Tensor) -> torch.Tensor:
		# 编码器部分
		x1 = F.relu(self.enc_conv1(x))
		x2 = self.pool(x1)

		x2 = F.relu(self.enc_conv2(x2))
		x3 = self.pool(x2)

		x3 = F.relu(self.enc_conv3(x3))
		x4 = self.pool(x3)

		x4 = F.relu(self.enc_conv4(x4))

		# 解码器部分
		x = self.up(x4)
		x = F.relu(self.dec_conv1(x))

		x = self.up(x)
		x = F.relu(self.dec_conv2(x))

		x = self.up(x)
		x = F.relu(self.dec_conv3(x))

		x = self.dec_conv4(x)
		x = torch.sigmoid(x)

		return x


def load_official_model(device: torch.device) -> nn.Module:
	"""加载官方 RMBG-2.0 模型（推荐）"""
	if not TRANSFORMERS_AVAILABLE:
		raise ImportError("需要安装 transformers 库: pip install transformers")
	
	# 设置模型缓存目录为项目根目录下的 models 文件夹
	models_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')
	os.makedirs(models_dir, exist_ok=True)
	
	print(f"[信息] 正在从 Hugging Face 加载官方 RMBG-2.0 模型...")
	print(f"[信息] 模型将保存到: {models_dir}")
	
	model = AutoModelForImageSegmentation.from_pretrained(
		'briaai/RMBG-2.0', 
		trust_remote_code=True,
		cache_dir=models_dir
	)
	torch.set_float32_matmul_precision('high')
	model.to(device)
	model.eval()
	print("[信息] 官方模型加载完成")
	return model


def load_demo_model(weights_path: Optional[str], device: torch.device) -> nn.Module:
	"""加载演示用的简单 U-Net 模型"""
	model = BriaRMBG().to(device)
	if weights_path:
		# 如果路径不是绝对路径，则相对于项目根目录查找
		if not os.path.isabs(weights_path):
			project_root = os.path.dirname(os.path.abspath(__file__))
			weights_path = os.path.join(project_root, weights_path)
		
		if not os.path.isfile(weights_path):
			raise FileNotFoundError(f"找不到权重文件: {weights_path}")
		
		print(f"[信息] 正在加载演示模型权重: {weights_path}")
		state = torch.load(weights_path, map_location=device)
		# 兼容 state_dict 或完整对象
		if isinstance(state, dict) and 'state_dict' in state:
			state = state['state_dict']
		model.load_state_dict(state, strict=False)
		print("[信息] 演示模型权重加载完成")
	else:
		print("[警告] 未提供权重文件，将使用随机初始化权重，仅用于流程验证。")
	model.eval()
	return model


def infer_single_image_official(model: nn.Module, image_path: str, device: torch.device, input_size: int) -> np.ndarray:
	"""使用官方模型进行推理"""
	image = Image.open(image_path)
	original_size = (image.height, image.width)
	
	# 官方模型的预处理
	transform = transforms.Compose([
		transforms.Resize((input_size, input_size)),
		transforms.ToTensor(),
		transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
	])
	
	input_tensor = transform(image).unsqueeze(0).to(device)
	
	with torch.no_grad():
		preds = model(input_tensor)[-1].sigmoid().cpu()
	
	pred = preds[0].squeeze()
	pred_pil = transforms.ToPILImage()(pred)
	mask = pred_pil.resize(original_size)
	mask = np.array(mask)
	return mask


def infer_single_image_demo(model: nn.Module, image_path: str, device: torch.device, input_size: int) -> np.ndarray:
	"""使用演示模型进行推理"""
	image = Image.open(image_path)
	original_size = (image.height, image.width)
	input_tensor = preprocess_image(image, (input_size, input_size)).to(device)
	with torch.no_grad():
		pred = model(input_tensor)
	mask = resize_mask_to_original(pred, original_size)
	return mask


def save_mask(mask: np.ndarray, out_path: str) -> None:
	Image.fromarray(mask).save(out_path)


def save_rgba_with_alpha(original_path: str, mask: np.ndarray, out_path: str) -> None:
	img = Image.open(original_path)
	if img.mode != 'RGBA':
		img = img.convert('RGBA')
	alpha = Image.fromarray(mask, mode='L')
	r, g, b, _ = img.split()
	Image.merge('RGBA', (r, g, b, alpha)).save(out_path)


def load_config(config_file="config.json"):
	"""从config.json文件加载配置"""
	if not os.path.exists(config_file):
		print(f"警告：配置文件 {config_file} 不存在，将使用命令行参数")
		return None
	
	try:
		with open(config_file, 'r', encoding='utf-8') as f:
			config = json.load(f)
		return config
	except Exception as e:
		print(f"读取配置文件失败: {e}")
		return None


def get_config_value(config, section, key, default_value):
	"""从配置中获取值，如果不存在则返回默认值"""
	if config and section in config and key in config[section]:
		return config[section][key]
	return default_value


def collect_images(input_path: str) -> List[str]:
	p = Path(input_path)
	if p.is_file():
		return [str(p)]
	if not p.exists():
		raise FileNotFoundError(f"输入路径不存在: {input_path}")
	imgs = []
	for ext in ["*.png", "*.jpg", "*.jpeg", "*.bmp", "*.webp"]:
		imgs.extend([str(x) for x in p.rglob(ext)])
	return imgs


def ensure_dir(path: str) -> None:
	os.makedirs(path, exist_ok=True)


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="RMBG2.0 本地推理脚本")
	parser.add_argument("--input", required=False, help="输入图片路径或文件夹（如果不提供，将从config.json读取）")
	parser.add_argument("--output", required=False, help="输出目录或文件路径（如果不提供，将从config.json读取）")
	parser.add_argument("--config", default="config.json", help="配置文件路径")
	parser.add_argument("--model", default="official", choices=["official", "demo"], 
						help="模型类型：official=官方RMBG-2.0（推荐），demo=简单演示模型")
	parser.add_argument("--weights", required=False, default=None, 
						help="仅demo模式需要：权重文件路径，如 models/demo.pth。不提供则使用随机权重")
	parser.add_argument("--size", type=int, default=1024, help="模型输入的方形边长，官方推荐1024，demo可用320/512")
	parser.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"], help="推理设备")
	parser.add_argument("--save-mask", action="store_true", help="仅保存灰度掩码，不合成透明PNG")
	parser.add_argument("--both", action="store_true", help="同时保存掩码与透明PNG")
	return parser.parse_args()


def select_device(kind: str) -> torch.device:
	if kind == "cpu":
		return torch.device("cpu")
	if kind == "cuda":
		return torch.device("cuda" if torch.cuda.is_available() else "cpu")
	# auto
	return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def main() -> None:
	args = parse_args()
	device = select_device(args.device)
	print(f"[信息] 使用设备: {device}")

	# 加载配置文件
	config = load_config(args.config)
	
	# 确定输入和输出路径
	input_path = args.input
	output_path = args.output
	
	if not input_path and config:
		input_path = get_config_value(config, "图片去背景", "INPUT_PATH", "input/test.png")
		print(f"[信息] 从配置文件读取输入路径: {input_path}")
	
	if not output_path and config:
		output_path = get_config_value(config, "图片去背景", "OUTPUT_PATH", "output/rmbg_output")
		print(f"[信息] 从配置文件读取输出路径: {output_path}")
	
	if not input_path:
		raise RuntimeError("请提供输入路径参数或确保config.json中包含INPUT_PATH配置")
	
	if not output_path:
		output_path = "output/rmbg_output"
		print(f"[信息] 使用默认输出路径: {output_path}")
	
	# 从配置文件读取SAVE_BOTH参数
	save_both = get_config_value(config, "图片去背景", "SAVE_BOTH", True)
	if save_both and not args.save_mask and not args.both:
		args.both = True
		print(f"[信息] 从配置文件读取SAVE_BOTH: {save_both}，将同时保存掩码和透明图")

	# 加载模型
	if args.model == "official":
		model = load_official_model(device)
		infer_fn = infer_single_image_official
	else:  # demo
		model = load_demo_model(args.weights, device)
		infer_fn = infer_single_image_demo

	image_paths = collect_images(input_path)
	if len(image_paths) == 0:
		raise RuntimeError("未在输入路径下找到任何图像文件")

	# 判断输出是目录还是单一文件
	output_path = Path(output_path)
	save_as_single_file = Path(input_path).is_file() and (output_path.suffix.lower() in [".png", ".jpg", ".jpeg", ".bmp", ".webp"])

	if save_as_single_file:
		ensure_dir(str(output_path.parent))
	else:
		ensure_dir(str(output_path))

	for img_path in image_paths:
		mask = infer_fn(model, img_path, device, args.size)

		if save_as_single_file and len(image_paths) == 1:
			if args.save_mask and not args.both:
				save_mask(mask, str(output_path))
			else:
				save_rgba_with_alpha(img_path, mask, str(output_path))
			print(f"完成: {img_path} -> {output_path}")
			continue

		# 使用固定文件名，覆盖上一次保存的文件
		if args.save_mask or args.both:
			mask_out = (output_path / "mask.png").as_posix() if not save_as_single_file else str(output_path)
			save_mask(mask, mask_out)
			print(f"保存掩码: {img_path} -> {mask_out}")

		if not args.save_mask or args.both:
			rgba_out = (output_path / "rgba.png").as_posix() if not save_as_single_file else str(output_path)
			save_rgba_with_alpha(img_path, mask, rgba_out)
			print(f"保存透明图: {img_path} -> {rgba_out}")

	print("全部完成。")


if __name__ == "__main__":
	main()


