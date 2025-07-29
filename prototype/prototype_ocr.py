#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OCR文字识别原型
通过输入图片路径，使用OCR解析图片中的文字内容
"""

import os
import sys
from PIL import Image
import pytesseract
from datetime import datetime


class OCRTextExtractor:
    """OCR文字提取器"""
    
    def __init__(self):
        """初始化OCR提取器"""
        self.supported_formats = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif'}
        
    def extract_text_from_image(self, image_path):
        """从图片中提取文字
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            tuple: (success, text, error_message)
        """
        try:
            # 验证文件路径
            if not os.path.exists(image_path):
                return False, None, f"图片文件不存在: {image_path}"
            
            # 验证文件格式
            file_ext = os.path.splitext(image_path)[1].lower()
            if file_ext not in self.supported_formats:
                return False, None, f"不支持的图片格式: {file_ext}"
            
            print(f"📸 正在加载图片: {image_path}")
            
            # 加载图片
            image = Image.open(image_path)
            print(f"✅ 图片加载成功: {image.size}")
            
            # 执行OCR识别
            print("🔍 正在进行OCR文字识别...")
            extracted_text = pytesseract.image_to_string(image, lang='chi_sim+eng')
            
            # 清理识别结果
            cleaned_text = extracted_text.strip()
            
            if cleaned_text:
                print(f"✅ OCR识别完成，共识别 {len(cleaned_text)} 个字符")
                return True, cleaned_text, None
            else:
                return False, None, "未识别到任何文字内容"
                
        except Exception as e:
            error_msg = f"OCR识别失败: {str(e)}"
            print(f"❌ {error_msg}")
            return False, None, error_msg
    
    def process_image(self, image_path):
        """处理图片并输出结果
        
        Args:
            image_path: 图片文件路径
        """
        print("🔤 OCR文字识别工具")
        print("=" * 40)
        
        success, text, error = self.extract_text_from_image(image_path)
        
        if success:
            print("\n📝 识别结果:")
            print("-" * 40)
            print(text)
            print("-" * 40)
            print(f"📊 统计信息:")
            print(f"   字符总数: {len(text)}")
            print(f"   行数: {len(text.splitlines())}")
            print(f"   处理时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"\n❌ 识别失败: {error}")


def main():
    """主程序入口"""
    if len(sys.argv) != 2:
        print("📖 使用方法:")
        print(f"   python {os.path.basename(__file__)} <图片路径>")
        print("\n📝 示例:")
        print(f"   python {os.path.basename(__file__)} /path/to/image.png")
        print(f"   python {os.path.basename(__file__)} screenshot.jpg")
        print("\n🎯 支持格式: PNG, JPG, JPEG, BMP, TIFF, GIF")
        return
    
    image_path = sys.argv[1]
    
    try:
        ocr_extractor = OCRTextExtractor()
        ocr_extractor.process_image(image_path)
        
    except KeyboardInterrupt:
        print("\n👋 程序已退出")
    except Exception as e:
        print(f"\n❌ 程序错误: {str(e)}")


if __name__ == "__main__":
    main()