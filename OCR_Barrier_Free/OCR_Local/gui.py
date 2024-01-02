
import sys
import datetime
import os
import keyboard
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QPushButton, QTextEdit
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QScreen,QCursor
from PyQt5 import QtCore, QtGui, QtWidgets
from sample import Sample
from sample import Sample
from tts import TTSThread

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080) 
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # 用户名输入框
        self.usernameInput =QtWidgets.QLineEdit(self.centralwidget)
        self.usernameInput.setGeometry(QtCore.QRect(50, 50, 400, 30))
        self.usernameInput.setObjectName("usernameInput")
        self.usernameInput.setStyleSheet("border: 1px solid red;")
        self.usernameInput.setEchoMode(QtWidgets.QLineEdit.Password)  # 设置为密码模式，文本以星号显示

        # 密码输入框
        self.passwordInput = QtWidgets.QLineEdit(self.centralwidget)
        self.passwordInput.setGeometry(QtCore.QRect(50, 100, 400, 30)) # Adjust the position and size as needed
        self.passwordInput.setObjectName("passwordInput")
        self.passwordInput.setStyleSheet("border: 1px solid red;")
        self.passwordInput.setEchoMode(QtWidgets.QLineEdit.Password)  # 设置为密码模式，文本以星号显示

        # 图片路径
        self.imagepathInput = QtWidgets.QLineEdit(self.centralwidget)
        self.imagepathInput.setGeometry(QtCore.QRect(50, 150, 400, 30)) # Adjust the position and size as needed
        self.imagepathInput.setObjectName("imagepathInput")
        self.imagepathInput.setStyleSheet("border: 1px solid red;")

        # 添加截图按钮
        self.snipButton = QtWidgets.QPushButton(self.centralwidget)
        self.snipButton.setGeometry(QtCore.QRect(50, 250, 400, 40))
        self.snipButton.setObjectName("snipButton")
        self.snipButton.setText("截图")
        self.snipButton.setStyleSheet("border: 1px solid blue;")
        self.snipButton.clicked.connect(self.captureScreen_screenshot)

        # 提交按钮
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(50, 200, 400, 40)) # Adjust the position and size as needed
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet("border: 1px solid red;")
        # self.pushButton.setShortcut('P')  # 将回车键设置为快捷键
        # 为按钮添加功能
        self.pushButton.clicked.connect(self.displayText)
        

        # Large Text Area with yellow border
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(500, 50, 1400, 800)) # Adjust the position and size as needed
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setStyleSheet("border: 2px solid orange;")

        

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def captureScreen_screenshot(self):
        self.snipWidget = SnipWidget()
        self.snipWidget.screenshotTaken.connect(self.processScreenshot)

    def captureScreen(self):
        screen = QApplication.primaryScreen()
        screenshot = screen.grabWindow(0)
        cursor_position = QCursor.pos()
        rect = QtCore.QRect(cursor_position.x() - 50, cursor_position.y() - 50, 500, 100)
        cropped_screenshot = screenshot.copy(rect)
        self.processScreenshot(cropped_screenshot)

    def processScreenshot(self, screenshot):
        # 保存截图
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"screenshots/screenshot_{timestamp}.png"
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        screenshot.save(screenshot_path, 'PNG')
        print("截图成功")

        # 将截图的路径传递给OCR系统
        self.performOCR(screenshot_path)

    # 显示截图的文本
    def performOCR(self,screenshot_path):
        paragraph_text = None  # 或者其他适当的初始值
        try:
            paragraph_text = Sample.main("","",screenshot_path,sys.argv[1:])  # 传递除了脚本名之外的所有命令行参数
            # paragraph_text = Sample.main(self.usernameInput.text(),self.passwordInput.text(),screenshot_path,sys.argv[1:])  # 传递除了脚本名之外的所有命令行参数
        except Exception as e:
            print(e)
            error = e
        # paragraph_text = "不存在"
        # 清空图片路径输入框
        self.imagepathInput.setText('')
        if paragraph_text is not None:
            # input_text = """"第二届世界互联网大会将于2015年12月16日至18日在浙江省嘉兴市桐乡市乌镇举行。大会的主题是"互联互通、共享共治，共建网络空间命运共同体”。中国政府对此次大会高度重视，中共中央总书记、中国国家主席习近平将出席大会，并发表主旨演讲。"""
            input_text = paragraph_text
            self.textEdit.setText(input_text)
            # 创建TTS线程并开始播放
            self.tts_thread = TTSThread(input_text)
            self.tts_thread.start()
        else:
            input_text = f"{error}"
            self.textEdit.setText(input_text)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "UI"))
        self.pushButton.setText(_translate("MainWindow", "提交"))
        
    
    # 在textEdit控件中显示文本的函数
    def displayText(self):
        paragraph_text = None  # 或者其他适当的初始值
        try:
            paragraph_text = Sample.main(self.usernameInput.text(),self.passwordInput.text(),self.imagepathInput.text(),sys.argv[1:])  # 传递除了脚本名之外的所有命令行参数
        except Exception as e:
            print(e)
            error = e
        # paragraph_text = True
        # # 清空图片路径输入框
        self.imagepathInput.setText('')
        if paragraph_text is not None:
            input_text = """"第二届世界互联网大会将于2015年12月16日至18日在浙江省嘉兴市桐乡市乌镇举行。大会的主题是"互联互通、共享共治，共建网络空间命运共同体”。中国政府对此次大会高度重视，中共中央总书记、中国国家主席习近平将出席大会，并发表主旨演讲。"""
            input_text = paragraph_text
            self.textEdit.setText(input_text)
            # 创建TTS线程并开始播放
            self.tts_thread = TTSThread(input_text)
            self.tts_thread.start()
        else:
            input_text = f"{error}"
            self.textEdit.setText(input_text)

# 截图类   
class SnipWidget(QtWidgets.QWidget):
    screenshotTaken = QtCore.pyqtSignal(QtGui.QPixmap)  # 创建一个信号
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowOpacity(0.3)
        self.setGeometry(QtWidgets.QApplication.desktop().availableGeometry())
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), 2))
        qp.setBrush(QtGui.QColor(128, 128, 128, 128))
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.close()
        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        screenshot = QtWidgets.QApplication.primaryScreen().grabWindow(0, x1, y1, x2-x1, y2-y1)
        self.screenshotTaken.emit(screenshot)  # 发送信号，带有截图数据

    # def takeScreenshot(self, x, y, width, height):
    #     screenshot = QtWidgets.QApplication.primaryScreen().grabWindow(0, x, y, width, height)
    #     screenshot.save('screenshot.png', 'png')

# 重写主类
class MyMainWindow(QtWidgets.QMainWindow):
    key_pressed_signal = pyqtSignal()
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.key_pressed_signal.connect(self.ui.captureScreen_screenshot)
        # 设置全局按键监听
        keyboard.on_press(self.on_key_press)

    def mousePressEvent(self, event):
        # 当点击非输入框区域时，使所有输入框失去焦点
        if not self.ui.usernameInput.underMouse():
            self.ui.usernameInput.clearFocus()
        if not self.ui.passwordInput.underMouse():
            self.ui.passwordInput.clearFocus()
        if not self.ui.imagepathInput.underMouse():
            self.ui.imagepathInput.clearFocus()
        if not self.ui.textEdit.underMouse():
            self.ui.textEdit.clearFocus()
        super(MyMainWindow, self).mousePressEvent(event)
    
    # 全局截图功能
    def on_key_press(self, event):
        if event.name == 'p':
            self.key_pressed_signal.emit()

    # 局部截图（重写）
    # def keyPressEvent(self, event):
    #     if event.key() == QtCore.Qt.Key_P:  
    #         self.key_pressed_signal.emit()  


# def on_key_press(key):
#     if key.name == 'p':op
#         global mainWin
#         mainWin.key_pressed_signal.emit()  

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # keyboard.on_press_key('p', on_key_press)

    mainWin = MyMainWindow()
    mainWin.show()
    sys.exit(app.exec_())