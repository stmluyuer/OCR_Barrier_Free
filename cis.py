import cv2
import numpy as np
import mss
from PIL import ImageGrab
import pyautogui
import time
from pywinauto import Application
from pywinauto import mouse
import ctypes
import sys

# 检查管理员权限运行
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        # 重新运行管理员
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

# 管理员权限运行
run_as_admin()

# 初始化 Application 
app = Application()
# 连接
app.connect(title="逍遥模拟器")  
window = app['逍遥模拟器']  

# 定义要匹配的色块的颜色范围
target_color = np.array([89, 253, 168])
tolerance = np.array([30, 30, 30])
# 定义颜色范围的上界
lower_blue = np.array([target_color[0] - 30, target_color[1] - 30, target_color[2] - 30])

# 定义颜色范围的下界
upper_blue = np.array([target_color[0] + 5, target_color[1] + 5, target_color[2] + 5])

# 设置截图区域
top, left, width, height = 0, 0, 2560, 1600

# 模板路径
soft_drink_template_file = '01.jpg'
crisps_template_file = '02.jpg'


# 加载障碍物的模板图像
soft_drink_template = cv2.imread(soft_drink_template_file, cv2.IMREAD_GRAYSCALE)
crisps_template = cv2.imread(crisps_template_file, cv2.IMREAD_GRAYSCALE)

# 定义障碍物列表
obstacles = [
    {
        'template': soft_drink_template,
        'file': soft_drink_template_file,
        'action': '操作1'
    },
    {
        'template': crisps_template,
        'file': crisps_template_file,
        'action': '操作2'
    },
    # 添加更多障碍物...
]

# 定义模板匹配的阈值
threshold = 0.8

enable_neighbor_check = True

# 创建屏幕截图对象
with mss.mss() as sct:
    # 定义全局变量
    cv_character_positions = None

    while True:
        key = cv2.waitKey(1)
        if key == 27:
            break
            # 获取屏幕截图
        screenshot = pyautogui.screenshot()

        # 转换
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # 将图像转换为HSV
        hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 白，黑
        mask = cv2.inRange(hsv_image, lower_blue, upper_blue)

        #形态学，去噪
        kernel = np.ones((5, 5), np.uint8)
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

        # 查寻轮廓
        contours, hierarchy = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # 遍历找到的轮廓
        for contour in contours:
            # 获取轮廓的包围矩形框的坐标
            x, y, w, h = cv2.boundingRect(contour)

            # 获取指定点的颜色
            target_point_color = frame[y, x]
            
            # 检查周围像素颜色是否接近目标点的颜色
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx == 0 and dy == 0:
                        continue

                    # 计算相邻点的坐标
                    neighbor_x = x + dx
                    neighbor_y = y + dy

                    if enable_neighbor_check:
                        # 检查相邻点是否在图像范围内
                        if 0 <= neighbor_x < frame.shape[1] and 0 <= neighbor_y < frame.shape[0]:
                            neighbor_color = frame[neighbor_y, neighbor_x]

                            # 计算颜色之间的差异
                            color_diff = np.abs(target_point_color - neighbor_color)

                            # 判断颜色差异是否在容许范围内
                            if np.all(color_diff <= tolerance):
                                # 计算Neighbor Position的平均值（不保留小数）
                                average_position = np.mean([(neighbor_x, neighbor_y)], axis=0).astype(int)
                                cv_character_positions = average_position
                                enable_neighbor_check = False  # 关闭开关，阻止后续的循环部分执行
                                print("Character Position:", cv_character_positions)
                                # 退出整个循环
                                break

                else:
                    continue
                break

            if cv_character_positions is not None:


                x = cv_character_positions[0]
                y = cv_character_positions[1] - 330
                # 获取屏幕截图  
                screenshot = sct.grab(sct.monitors[0])

                # 转换
                frame = np.array(screenshot)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                # 将图像转换为灰度图像
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # 设置阈值
                distance_threshold = 500

                # 遍历匹配位置，并进行相应操作
                for obstacle in obstacles:
                    template = obstacle['template']
                    template_file = obstacle['file']
                    action = obstacle['action']

                    # 根据模板进行匹配
                    res = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)
                    loc = np.where(res >= threshold)

                    # 遍历障碍物的匹配位置
                    for pt in zip(*loc[::-1]):
                        obstacle_x = pt[0]
                        obstacle_y = pt[1]

                        # 计算障碍物中心坐标
                        obstacle_center_x = obstacle_x + template.shape[1] // 2
                        obstacle_center_y = obstacle_y + template.shape[0] // 2
                        print("Obstacle Center:", (obstacle_center_x, obstacle_center_y))


                        if (
                            -50 < cv_character_positions[0] - obstacle_center_x < 50
                            and 250 < cv_character_positions[1] - obstacle_center_y < 500
                        ):  
                            # 执行鼠标点击操作
                            window.click_input(coords=(280, 1090))  # 替换为实际的鼠标点击函数或操作
                            print("Performing action:", action)

                if cv2.waitKey(1) == 27:
                    break

# 关闭窗口
cv2.destroyAllWindows()