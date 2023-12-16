from pynput import keyboard
from PIL import ImageGrab
import base64
import requests
import io
import json

def on_press(key):
    try:
        if key == keyboard.Key.f9:
            # 捕获屏幕截图
            screenshot = ImageGrab.grab()
            buffer = io.BytesIO()
            screenshot.save(buffer, format="JPEG")
            img_base64 = base64.b64encode(buffer.getvalue())

            # 发送请求到 OCR 接口
            response = requests.post("http://127.0.0.1:19811/ocr2", data=img_base64)
            
            # 处理响应
            if response.status_code == 200:
                ocr_data = response.text
                print("识别结果:", ocr_data)
            else:
                print("请求失败，状态码:", response.status_code)
    except Exception as e:
        print("发生错误:", e)

# 监听键盘事件
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
