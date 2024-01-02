import sys
from PyQt5 import QtWidgets, QtCore, QtGui

class SnipWidget(QtWidgets.QWidget):
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

        self.takeScreenshot(x1, y1, x2-x1, y2-y1)

    def takeScreenshot(self, x, y, width, height):
        screenshot = QtWidgets.QApplication.primaryScreen().grabWindow(0, x, y, width, height)
        screenshot.save('screenshot.png', 'png')

def main():
    app = QtWidgets.QApplication(sys.argv)
    snip = SnipWidget()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
