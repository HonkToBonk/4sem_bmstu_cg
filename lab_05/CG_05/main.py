from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QImage, QPixmap, QPainter
from os import startfile
import design
import time
from math import ceil, floor

class myApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super(myApp, self).__init__()
        self.setupUi(self)
        self.scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        self.sceneWidth = self.graphicsView.width()
        self.sceneHeight = self.graphicsView.height()
        self.graphicsView.setSceneRect(0, 0, self.sceneWidth - 10, self.sceneHeight - 10)
        self.image = QImage(self.sceneWidth, self.sceneHeight, QImage.Format_RGB32)
        self.image.fill(QtCore.Qt.white)
        self.painter = QPainter()
        self.painter.begin(self.image)
        self.painter.setPen(QtCore.Qt.black)
        self.painter.drawImage(0, 0, self.image)

        self.process = False
        self.lastKeys = [0, 0]
        self.mode = 'null'
        self.figure = []
        self.method = "no delay"
        self.barier = []
        self.xPrev = -1
        self.yPrev = -1
        self.xCur = -1
        self.yCur = -1

        self.paintBut.clicked.connect(self.paint)
        self.clean.clicked.connect(self.clean_screen)
        self.cancel.clicked.connect(self.cancel_painting)
        self.inputMode.clicked.connect(self.modeChange)

    def reDraw(self):
        self.pixmap = QPixmap.fromImage(self.image)
        self.scene.clear()
        self.scene.addPixmap(self.pixmap)

    def reDrawFig(self, mode):
        if mode == "clear":
            self.image.fill(QtCore.Qt.white)
        self.setColor()
        for i in range(len(self.figure)):
            for j in range(len(self.figure[i]) - 1):
                self.xCur, self.xNext = self.figure[i][j][0], self.figure[i][j + 1][0]
                self.yCur, self.yNext = self.figure[i][j][1], self.figure[i][j + 1][1]
                self.painter.drawLine(self.xCur, self.yCur, self.xNext, self.yNext)
        if mode != "no_redraw":
            self.reDraw()

    def mousePressEvent(self, event):
        x = event.x() - 20
        y = event.y() - 16
        if 0 <= x <= self.sceneWidth - 10 and 0 <= y <= self.sceneHeight - 10 and self.mode == 'start':
            self.xPrev, self.yPrev = self.xCur, self.yCur
            if self.horizontal.isChecked():
                self.xCur, self.yCur = x, self.yPrev
            elif self.vertical.isChecked():
                self.xCur, self.yCur = self.xPrev, y
            elif self.nomode.isChecked():
                self.xCur, self.yCur = x, y
            if self.mode == 'start':
                # print("Current point [{0}, {1}]".format(self.xCur, self.yCur))
                self.figure[len(self.figure) - 1].append([self.xCur, self.yCur])
                self.painter.drawPoint(self.xCur, self.yCur)
                if self.xPrev != -1 and self.yPrev != -1:
                    self.painter.drawLine(self.xCur, self.yCur, self.xPrev, self.yPrev)
        elif 0 <= x <= self.sceneWidth - 10 and 0 <= y <= self.sceneHeight - 10 and self.mode != 'start':
            self.showError(1)
        self.reDraw()

    def modeChange(self):
        if not self.process:
            if self.mode != 'start':
                self.inputMode.setStyleSheet("background-color : lightgray")
                self.mode = 'start'
                self.xCur, self.yCur, self.xPrev, self.yPrev = -1, -1, -1, -1
                self.figure.append([])
            elif self.mode == 'start':
                if len(self.figure[len(self.figure) - 1]) < 3:
                    self.showError(2)
                else:
                    self.inputMode.setStyleSheet("")
                    self.mode = 'end'
                    self.figure[len(self.figure) - 1].append(
                        [self.figure[len(self.figure) - 1][0][0], self.figure[len(self.figure) - 1][0][1]])
                    self.painter.drawLine(self.xCur, self.yCur, self.figure[len(self.figure) - 1][0][0],
                                          self.figure[len(self.figure) - 1][0][1])
                    self.xCur, self.yCur, self.xPrev, self.yPrev = -1, -1, -1, -1
                    self.setColor()
                    self.reDrawFig("clear")
                    self.reDraw()

    def paint(self):
        if not self.process and self.mode == 'end':
            self.process = True
            self.setColor()
            self.setMode()
            self.reDrawFig("clear")

            start = time.time()
            self.findBariers()
            for i in range(len(self.figure)):
                self.paintOneFig(i)
            self.reDrawFig("not")
            end = time.time()

            self.setColor()
            self.process = False

            time_info = QtWidgets.QMessageBox()
            time_info.setWindowTitle("Информация")
            time_info.setText("Закраска выполнена за {0:.3f} секунд".format(end - start))
            time_info.setIcon(QtWidgets.QMessageBox.Information)
            time_info.exec_()
        elif self.mode != 'end':
            self.showError(2)

    def findBariers(self):
        self.barier.clear()
        for i in range(len(self.figure)):
            curMax, curMin = self.figure[i][0][0], self.figure[i][0][0]
            for j in range(1, len(self.figure[i]) - 1):
                if self.figure[i][j][0] > curMax:
                    curMax = self.figure[i][j][0]
                if self.figure[i][j][0] < curMin:
                    curMin = self.figure[i][j][0]
            curBar = (curMax + curMin) / 2
            self.barier.append(int(curBar))

    def paintOneFig(self, ind):
        curBar = self.barier[ind]
        prevDy, firstDy = 0, 0
        for i in range(len(self.figure[ind]) - 1):
            xCur, xNext = self.figure[ind][i][0], self.figure[ind][i + 1][0]
            yCur, yNext = self.figure[ind][i][1], self.figure[ind][i + 1][1]
            if yCur != yNext:
                dy = self.sign(yCur, yNext)
                if i == 0:
                    firstDy = dy
                dx = (xNext - xCur) / abs(yNext - yCur)
                x = xCur
                if yNext > yCur:
                    yNext += 1
                    if dy == prevDy:
                        yCur += 1
                    if i == len(self.figure[ind]) - 2 and dy == firstDy:
                        yNext -= 1
                if yNext < yCur:
                    yNext -= 1
                    if dy == prevDy:
                        yCur -= 1
                    if i == len(self.figure[ind]) - 2 and dy == firstDy:
                        yNext += 1
                prevDy = dy
                for j in range(yCur, yNext, dy):
                    if x < curBar:
                        for k in range(floor(x), curBar):
                            self.checkPixel(k, j)
                    else:
                        for k in range(curBar, ceil(x)):
                            self.checkPixel(k, j)
                    x += dx

                    if self.method == "delay" and self.delay.text() == "gosha":
                        startfile("C:/msys64/home/BarDuck/ComGr/lab_05/Temp/gosha.mp4")
                        self.cancel_painting()
                        return
                    try:
                        if self.method == "delay" and int(self.delay.text()) > 0:
                            self.reDrawFig("no_redraw")
                            self.reDraw()
                            self.wait(int(self.delay.text()))
                        elif self.method == "delay":
                            self.showError(3)
                            self.cancel_painting()
                            return
                    except:
                        if self.method == "delay":
                            self.showError(3)
                            self.cancel_painting()
                            return

    def wait(self, t):
        loop = QtCore.QEventLoop()
        QtCore.QTimer.singleShot(t, loop.quit)
        loop.exec_()

    def sign(self, x1, x2):
        if x1 > x2:
            return -1
        else:
            return 1

    def mathRound(self, x):
        if x >= 0:
            return int(x + 0.5)
        else:
            return int(x - 0.5)

    def setColor(self):
        color = self.colorBox.currentIndex()
        if color == 0:
            self.painter.setPen(QtCore.Qt.black)
        elif color == 1:
            self.painter.setPen(QtCore.Qt.red)
        elif color == 2:
            self.painter.setPen(QtCore.Qt.green)
        else:
            self.painter.setPen(QtCore.Qt.blue)

    def setMode(self):
        method = self.paintBox.currentIndex()
        if method == 1:
            self.method = "no delay"
        else:
            self.method = "delay"

    def checkPixel(self, x, y):
        if self.image.pixelColor(x, y).name() == "#ffffff":
            self.setColor()
        else:
            self.painter.setPen(QtCore.Qt.white)
        self.painter.drawPoint(x, y)

    def showError(self, mode):
        error = QtWidgets.QMessageBox()
        error.setWindowTitle("Ошибка")
        if mode == 1:
            error.setText("Вы находитесь вне режима внесения точек фигуры.")
        elif mode == 2:
            error.setText("Фигура вырождена в прямую/точку или не дорисована. Добавьте вершин.")
        elif mode == 3:
            error.setText("Задержка должна быть целым числом больше 0.")
        error.setIcon(QtWidgets.QMessageBox.Warning)
        error.exec_()

    def clean_screen(self):
        self.mode = 'null'
        self.figure = []
        self.barier = []
        self.xCur, self.yCur, self.xPrev, self.yPrev = -1, -1, -1, -1
        self.image.fill(QtCore.Qt.white)
        self.reDraw()
        print('Clear all')

    def cancel_painting(self):
        self.image.fill(QtCore.Qt.white)
        self.reDrawFig("clear")
        self.reDraw()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = myApp()
    MainWindow.show()
    sys.exit(app.exec_())
