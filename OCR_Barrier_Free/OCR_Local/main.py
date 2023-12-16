from pynput import keyboard
from PIL import ImageGrab, Image, ImageDraw
import pytesseract
import numpy as np
import cv2

pytesseract.pytesseract.tesseract_cmd = r'D:\PATH\OCR\tesseract.exe'


try:
    # # 捕获屏幕截图
    # screenshot = ImageGrab.grab()
    # screenshot_np = np.array(screenshot)
    # screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)
    image_path = input("请输入图片路径: ")
    image_path = f'img/{image_path}.jpg'  # 替换成你的图片路径
    image = Image.open(image_path)
    # screenshot_np = np.array(image)
    # screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)
    # 使用 OCR 分析截图
    data = pytesseract.image_to_data(image, lang='chi_sim', output_type=pytesseract.Output.DICT)

    # # 获取每个识别文字的位置和文本
    # n_boxes = len(data['text'])
    # for i in range(n_boxes):
    #     if int(data['conf'][i]) > 60:  # 选择置信度高于某个阈值的结果
    #         (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
    #         text = data['text'][i]
    #         print(f"位置: ({x}, {y}), 宽度: {w}, 高度: {h}, 文本: {text}")

    # # 根据识别的位置信息组织文本
    # lines = {}
    # for i in range(n_boxes):
    #     if data['text'][i].strip():
    #         # 使用top坐标作为行的关键字
    #         line = lines.get(data['top'][i], [])
    #         line.append(data['text'][i])
    #         lines[data['top'][i]] = line

    # # 将同一行的文本拼接起来
    # for top in sorted(lines):
    #     print(" ".join(lines[top]))
    # 计算文本块的平均高度
    # 计算文本块的平均高度
    total_height = sum(data['height'][i] for i in range(len(data['text'])) if data['text'][i].strip())
    num_texts = sum(1 for i in range(len(data['text'])) if data['text'][i].strip())
    average_height = total_height / num_texts if num_texts else 0

    # 动态调整阈值
    threshold_factor = 1  # 可调整的因子
    threshold = average_height * threshold_factor

    # 判断两个文本块是否在同一行
    def in_same_line(y1, y2, threshold):
        return abs(y1 - y2) <= threshold

    # 组织文本为行
    lines = []
    for i in range(len(data['text'])):
        if data['text'][i].strip():  # 只考虑非空文本
            x, y, text = data['left'][i], data['top'][i], data['text'][i]

            # 查找当前文本块应该被放置的行
            found_row = False
            for line in lines:
                if in_same_line(line['top'], y, threshold):
                    line['text'].append(text)
                    found_row = True
                    break
            
            # 如果没有找到合适的行，创建新行
            if not found_row:
                lines.append({'top': y, 'text': [text]})

    # 按照 y 坐标排序行并输出
    for line in sorted(lines, key=lambda x: x['top']):
        print(" ".join(line['text']))
    # # 创建一个白色背景图像
    # whiteboard = Image.new('RGB', image.size, color=(255, 255, 255))
    # draw = ImageDraw.Draw(whiteboard)
    # original_data_text = data['text']
    # cleaned_data_text = [item for item in original_data_text if item.strip()]
    # print(data['text'])
    # print(cleaned_data_text)
    
    # 在白板上放置文本
    # n_boxes = len(data['text'])
    # for i in range(n_boxes):
    #     if int(data['conf'][i]) > 30:  # 置信度阈值
    #         (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
    #         text = data['text'][i]
    #         draw.text((x, y), text, fill=(0, 0, 0))

    # # 显示白板
    # save_path = r'img\whiteboard.png'
    # whiteboard.save(save_path)
    # whiteboard.show()

except Exception as e:
    print("发生错误:", e)
