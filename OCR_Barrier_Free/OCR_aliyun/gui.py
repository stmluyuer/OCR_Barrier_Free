
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from sample import Sample
from sample import Sample
from tts import TTSThread
# import pyttsx3

# class MyMainWindow(QtWidgets.QMainWindow):
#     def __init__(self, parent=None):
#         super(MyMainWindow, self).__init__(parent)
#         self.ui = Ui_MainWindow()  
#         self.ui.setupUi(self)

#     def mousePressEvent(self, event):
#         # 检查点击事件是否在输入框之外
#         if not self.ui.usernameInput.underMouse():
#             self.ui.usernameInput.clearFocus()
#         if not self.ui.passwordInput.underMouse():
#             self.ui.passwordInput.clearFocus()
#         super(MyMainWindow, self).mousePressEvent(event)

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

        # Button with red border
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
        # self.imagepathInput.setText('')
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
        


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = MyMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())