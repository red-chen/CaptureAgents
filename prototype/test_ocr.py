#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OCR原型测试脚本
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_ocr_prototype():
    """测试OCR原型功能"""
    print("🧪 OCR文字识别原型测试")
    print("=" * 40)
    print("✨ 功能特点:")
    print("   📸 支持多种图片格式 (PNG, JPG, JPEG, BMP, TIFF, GIF)")
    print("   🔤 使用pytesseract进行OCR识别")
    print("   🌏 支持中英文混合识别")
    print("   📊 提供详细的识别统计信息")
    print("   ⚡ 简单易用的命令行接口")
    print()
    
    # 检查是否有可用的测试图片
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    test_images = []
    
    # 查找桌面上的截图文件
    for file in os.listdir(desktop_path):
        if file.startswith("screenshot_") and file.endswith(".png"):
            test_images.append(os.path.join(desktop_path, file))
    
    if test_images:
        print(f"🔍 发现 {len(test_images)} 个可用的测试图片:")
        for i, img_path in enumerate(test_images[:3], 1):  # 只显示前3个
            print(f"   {i}. {os.path.basename(img_path)}")
        
        choice = input(f"\n选择测试图片 (1-{min(3, len(test_images))}) 或输入自定义路径: ").strip()
        
        if choice.isdigit() and 1 <= int(choice) <= min(3, len(test_images)):
            test_image = test_images[int(choice) - 1]
        else:
            test_image = choice
    else:
        test_image = input("请输入图片路径: ").strip()
    
    if test_image:
        print(f"\n🚀 开始测试OCR识别...")
        print(f"📁 目标图片: {test_image}")
        
        from prototype_ocr import OCRTextExtractor
        
        ocr_extractor = OCRTextExtractor()
        ocr_extractor.process_image(test_image)
    else:
        print("👋 测试已取消")

if __name__ == "__main__":
    test_ocr_prototype()