import requests
import json

# 替换成你的AccessKey ID和AccessKey Secret
ACCESS_KEY_ID = ''
ACCESS_KEY_SECRET = ''

url = "https://ocr-api.cn-hangzhou.aliyuncs.com"
params = {
    "Url": "img\1.jpg"
}

# 根据阿里云文档设置其他必要的头部或参数
response = requests.post(url, params=params, auth=(ACCESS_KEY_ID, ACCESS_KEY_SECRET))

# 检查响应状态码
if response.status_code == 200:
    print("成功响应：", response.json())
else:
    print("错误响应：", response.status_code)

    # 尝试获取错误详细信息
    try:
        error_details = response.json()
        print("详细错误信息：", json.dumps(error_details, indent=4))
    except json.JSONDecodeError:
        print("响应内容不是JSON格式，原始内容：", response.text)