#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
区域截图原型 - 通过鼠标选择区域进行截图
功能：
1. 70%透明度蒙皮，确保用户能准确看到要截图的内容
2. 鼠标拖拽选择区域
3. 回车确认截图
4. ESC取消操作
"""

import tkinter as tk
import pyautogui
from PIL import Image, ImageTk
import os
from datetime import datetime


class RegionScreenshot:
    def __init__(self):
        self.root = None
        self.canvas = None
        self.screenshot_image = None
        self.bg_image = None
        self.selected_region = None
        self.selecting = False
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0

    def start_selection(self):
        """启动区域选择"""
        try:
            print("🎯 启动区域选择...")
            print("💡 操作说明:")
            print("   - 拖拽鼠标选择截图区域")
            print("   - 按 Enter 确认截图")
            print("   - 按 ESC 取消操作")
            
            # 先截取整个屏幕作为背景
            print("📸 正在截取屏幕...")
            self.screenshot_image = pyautogui.screenshot()
            print(f"✅ 屏幕截取完成: {self.screenshot_image.size}")
            
            # 创建选择界面
            if self.create_overlay_window():
                # 等待用户操作
                self.root.mainloop()
                
                # 处理选择结果
                if self.selected_region:
                    return self.save_selected_region()
                else:
                    print("❌ 用户取消了选择")
                    return False, None, "用户取消了选择"
            else:
                return False, None, "创建选择界面失败"
                
        except Exception as e:
            print(f"❌ 区域选择失败: {str(e)}")
            return False, None, str(e)
        finally:
            if self.root:
                try:
                    self.root.destroy()
                except:
                    pass

    def create_alpha_mask(self, width, height, alpha=0.1):
        """创建带alpha透明度的蒙皮图像
        
        Args:
            width: 图像宽度
            height: 图像高度
            alpha: 透明度 (0.0-1.0, 0.1表示90%透明)
        
        Returns:
            PIL Image对象
        """
        # 创建RGBA图像，黑色背景
        mask_image = Image.new('RGBA', (width, height), (0, 0, 0, int(255 * alpha)))
        return mask_image

    def create_composite_image(self, bg_image, mask_regions):
        """合成背景图像和蒙皮区域
        
        Args:
            bg_image: 背景截图
            mask_regions: 需要添加蒙皮的区域列表 [(x1, y1, x2, y2), ...]
        
        Returns:
            合成后的PIL Image对象
        """
        # 复制背景图像
        composite = bg_image.copy().convert('RGBA')
        
        # 为每个蒙皮区域添加透明遮罩
        for x1, y1, x2, y2 in mask_regions:
            if x2 > x1 and y2 > y1:  # 确保区域有效
                # 创建该区域的蒙皮
                mask_width = x2 - x1
                mask_height = y2 - y1
                mask = self.create_alpha_mask(mask_width, mask_height, alpha=0.1)  # 90%透明
                
                # 将蒙皮合成到指定位置
                composite.paste(mask, (x1, y1), mask)
        
        return composite

    def create_overlay_window(self):
        """创建选择窗口"""
        try:
            # 创建全屏窗口
            self.root = tk.Tk()
            self.root.title("区域选择")
            self.root.attributes('-fullscreen', True)
            self.root.attributes('-topmost', True)
            self.root.configure(cursor='crosshair')
            
            # 获取屏幕尺寸
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            print(f"🖥️ 屏幕尺寸: {screen_width} x {screen_height}")
            
            # 调整截图尺寸匹配屏幕
            if self.screenshot_image.size != (screen_width, screen_height):
                print(f"🔧 调整截图尺寸: {self.screenshot_image.size} -> ({screen_width}, {screen_height})")
                self.screenshot_image = self.screenshot_image.resize(
                    (screen_width, screen_height), 
                    Image.Resampling.LANCZOS
                )
            
            # 创建画布
            self.canvas = tk.Canvas(
                self.root,
                width=screen_width,
                height=screen_height,
                highlightthickness=0,
                bd=0
            )
            self.canvas.pack()
            
            # 创建初始的全屏蒙皮合成图像
            full_mask_regions = [(0, 0, screen_width, screen_height)]
            self.composite_image = self.create_composite_image(self.screenshot_image, full_mask_regions)
            
            # 显示合成图像
            self.display_image = ImageTk.PhotoImage(self.composite_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.display_image, tags='background')
            
            # 绑定事件
            self.canvas.bind('<Button-1>', self.on_mouse_down)
            self.canvas.bind('<B1-Motion>', self.on_mouse_drag)
            self.canvas.bind('<ButtonRelease-1>', self.on_mouse_up)
            self.root.bind('<Return>', self.on_confirm)
            self.root.bind('<Escape>', self.on_cancel)
            
            # 添加操作提示
            self.canvas.create_text(
                screen_width // 2, 50,
                text="拖拽选择截图区域 | Enter确认 | ESC取消",
                fill='white', font=('Arial', 16, 'bold'), tags='hint'
            )
            
            self.root.focus_set()
            print("✅ 选择界面创建成功 (使用PIL Alpha透明)")
            return True
            
        except Exception as e:
            print(f"❌ 创建选择窗口失败: {str(e)}")
            return False

    def on_mouse_down(self, event):
        """鼠标按下开始选择"""
        self.selecting = True
        self.start_x = event.x
        self.start_y = event.y
        self.end_x = event.x
        self.end_y = event.y

    def on_mouse_drag(self, event):
        """鼠标拖拽更新选择区域"""
        if self.selecting:
            self.end_x = event.x
            self.end_y = event.y
            self.update_selection_display()

    def on_mouse_up(self, event):
        """鼠标释放完成选择"""
        if self.selecting:
            self.end_x = event.x
            self.end_y = event.y
            self.selecting = False
            self.update_selection_display()

    def update_selection_display(self):
        """更新选择区域显示"""
        # 清除之前的选择显示
        self.canvas.delete('selection')
        self.canvas.delete('background')
        
        # 计算选择区域
        x1 = min(self.start_x, self.end_x)
        y1 = min(self.start_y, self.end_y)
        x2 = max(self.start_x, self.end_x)
        y2 = max(self.start_y, self.end_y)
        
        screen_width = self.canvas.winfo_width()
        screen_height = self.canvas.winfo_height()
        
        # 创建蒙皮区域列表（除了选择区域外的所有区域）
        mask_regions = []
        
        # 上方区域
        if y1 > 0:
            mask_regions.append((0, 0, screen_width, y1))
        
        # 下方区域
        if y2 < screen_height:
            mask_regions.append((0, y2, screen_width, screen_height))
        
        # 左侧区域
        if x1 > 0:
            mask_regions.append((0, y1, x1, y2))
        
        # 右侧区域
        if x2 < screen_width:
            mask_regions.append((x2, y1, screen_width, y2))
        
        # 重新合成图像
        self.composite_image = self.create_composite_image(self.screenshot_image, mask_regions)
        self.display_image = ImageTk.PhotoImage(self.composite_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.display_image, tags='background')
        
        # 绘制选择框边框
        if abs(x2 - x1) > 5 and abs(y2 - y1) > 5:  # 只有当选择区域足够大时才显示
            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                outline='red', width=2, tags='selection'
            )
            
            # 显示选择区域尺寸
            width = abs(x2 - x1)
            height = abs(y2 - y1)
            self.canvas.create_text(
                x1, y1 - 20 if y1 > 20 else y1 + 20,
                text=f"{width} × {height}",
                fill='white', font=('Arial', 12, 'bold'),
                anchor='nw', tags='selection'
            )

    def on_confirm(self, event):
        """回车确认选择"""
        if hasattr(self, 'start_x') and abs(self.end_x - self.start_x) > 10 and abs(self.end_y - self.start_y) > 10:
            x1 = min(self.start_x, self.end_x)
            y1 = min(self.start_y, self.end_y)
            x2 = max(self.start_x, self.end_x)
            y2 = max(self.start_y, self.end_y)
            self.selected_region = (x1, y1, x2, y2)
            print(f"✅ 确认选择区域: ({x1}, {y1}) -> ({x2}, {y2})")
        else:
            print("⚠️ 请先选择一个有效区域")
            return
        self.root.quit()

    def on_cancel(self, event):
        """ESC取消选择"""
        print("❌ 用户取消选择")
        self.selected_region = None
        self.root.quit()

    def save_selected_region(self):
        """保存选择的区域"""
        try:
            if not self.selected_region:
                return False, None, "没有选择区域"
            
            x1, y1, x2, y2 = self.selected_region
            print(f"🔄 正在裁剪区域: ({x1}, {y1}) -> ({x2}, {y2})")
            
            # 从原始截图中裁剪选择的区域
            cropped = self.screenshot_image.crop((x1, y1, x2, y2))
            print(f"✅ 裁剪完成: {cropped.size}")
            
            # 保存到桌面
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            filepath = os.path.join(desktop_path, filename)
            
            cropped.save(filepath, 'PNG')
            file_size = os.path.getsize(filepath) / 1024  # KB
            
            print(f"💾 截图保存成功!")
            print(f"📁 文件路径: {filepath}")
            print(f"📏 图片尺寸: {cropped.size[0]} × {cropped.size[1]}")
            print(f"📦 文件大小: {file_size:.1f} KB")
            
            return True, filepath, None
            
        except Exception as e:
            error_msg = f"保存截图失败: {str(e)}"
            print(f"❌ {error_msg}")
            return False, None, error_msg


def main():
    """主程序入口"""
    print("📸 区域截图工具")
    print("=" * 40)
    
    try:
        screenshot_tool = RegionScreenshot()
        success, filepath, error = screenshot_tool.start_selection()
        
        if success:
            print(f"\n🎉 截图成功! 文件已保存到: {filepath}")
        else:
            print(f"\n💡 操作结果: {error}")
            
    except KeyboardInterrupt:
        print("\n👋 程序已退出")
    except Exception as e:
        print(f"\n❌ 程序错误: {str(e)}")


if __name__ == "__main__":
    main()