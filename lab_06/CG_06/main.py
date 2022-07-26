import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import design
import numpy as np
from math import fabs
import time

import random as rd
from playsound import playsound
import threading

class Visual(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.label.setPalette(QtGui.QPalette(QtCore.Qt.white))
        self.white = QtGui.QColor(QtCore.Qt.white)
        self.black = QtGui.QColor(QtCore.Qt.black)
        self.colour_fill = QtGui.QColor(QtCore.Qt.red)
        self.colour_edge = QtGui.QColor(QtCore.Qt.blue)
        self.labelColourFill.setPalette(QtGui.QPalette(QtCore.Qt.red))
        self.labelColourEdges.setPalette(QtGui.QPalette(QtCore.Qt.blue))

        self.pm = QtGui.QPixmap(820, 700)
        self.pm.fill(self.white)
        self.img = self.pm.toImage()

        self.objX = np.array([], dtype=int)
        self.objY = np.array([], dtype=int)
        self.buf_objX = np.array([], dtype=int)
        self.buf_objY = np.array([], dtype=int)
        self.pixel_x = 0
        self.pixel_y = 0
        self.stack = []
        self.pivas = False

        self.pushButtonScreenClean.clicked.connect(self.clean_screen)
        self.pushButtonChooseColourEdges.clicked.connect(self.choose_color_edge)
        self.pushButtonChooseColourFill.clicked.connect(self.choose_color_fill)
        self.pushButtonFill.clicked.connect(self.fill)
        self.pushButtonTime.clicked.connect(self.count_time)
        self.pushButtonClose.clicked.connect(self.close_fig)

    def bres_int(self, x_start, y_start, x_end, y_end):
        dx = x_end - x_start
        dy = y_end - y_start
        sx = sign(dx)
        sy = sign(dy)
        dx = fabs(dx)
        dy = fabs(dy)
        if dy >= dx:
            dx, dy = dy, dx
            fl = 1
        else:
            fl = 0
        f = 2 * dy - dx
        x = round(x_start)
        y = round(y_start)
        i = 1
        while i <= dx + 1:
            self.img.setPixel(x, y, self.colour_edge.rgb())
            if f >= 0:
                if fl == 1:
                    x += sx
                else:
                    y += sy
                f -= 2 * dx
            if f <= 0:
                if fl == 1:
                    y += sy
                else:
                    x += sx
                f += 2 * dy
            i += 1

    def choose_color_fill(self):
        self.colour_fill = QtWidgets.QColorDialog.getColor()
        self.labelColourFill.setPalette(QtGui.QPalette(self.colour_fill))

    def choose_color_edge(self):
        self.colour_edge = QtWidgets.QColorDialog.getColor()
        self.labelColourEdges.setPalette(QtGui.QPalette(self.colour_edge))

    def mousePressEvent(self, press):
        self.img = self.pm.toImage()
        if press.button() == QtCore.Qt.LeftButton:
            if self.verticalMode.isChecked() and self.objX.size > 0:
                self.objX = np.append(self.objX, self.objX[self.objX.size - 1])
                self.objY = np.append(self.objY, (press.pos() - self.label.pos()).y())
            elif self.horizontalMode.isChecked() and self.objX.size > 0:
                self.objX = np.append(self.objX, (press.pos() - self.label.pos()).x())
                self.objY = np.append(self.objY, self.objY[self.objY.size - 1])
            else:
                self.objX = np.append(self.objX, (press.pos() - self.label.pos()).x())
                self.objY = np.append(self.objY, (press.pos() - self.label.pos()).y())
            if self.objX.size >= 2:
                self.bres_int(self.objX[self.objX.size - 2], self.objY[self.objY.size - 2],
                              self.objX[self.objX.size - 1], self.objY[self.objY.size - 1])
        elif press.button() == QtCore.Qt.RightButton:
            self.pixel_x = (press.pos() - self.label.pos()).x()
            self.pixel_y = (press.pos() - self.label.pos()).y()
            self.stack.append(self.pixel_y)
            self.stack.append(self.pixel_x)
            self.img.setPixel(self.pixel_x, self.pixel_y, self.black.rgb())
        self.buf_objX = np.copy(self.objX)
        self.buf_objY = np.copy(self.objY)
        self.pm = self.pm.fromImage(self.img)
        self.label.setPixmap(self.pm)

    def keyPressEvent(self, press):
        self.img = self.pm.toImage()
        if int(press.key()) == QtCore.Qt.Key_P:
            pivas_info = QtWidgets.QMessageBox()
            pivas_info.setWindowTitle("🦐 Information 🦐")
            if not self.pivas:
                self.colour_fill = QtGui.QColor(QtCore.Qt.yellow)
                self.colour_edge = QtGui.QColor(QtCore.Qt.lightGray)
                self.labelColourFill.setPalette(QtGui.QPalette(QtCore.Qt.yellow))
                self.labelColourEdges.setPalette(QtGui.QPalette(QtCore.Qt.lightGray))
                pivas_info.setText("🍺 Pivas mode activated 🍺")
                self.pivas = True
                self.lineEditDelay.setText("10")
            else:
                self.colour_fill = QtGui.QColor(QtCore.Qt.red)
                self.colour_edge = QtGui.QColor(QtCore.Qt.blue)
                self.labelColourFill.setPalette(QtGui.QPalette(QtCore.Qt.red))
                self.labelColourEdges.setPalette(QtGui.QPalette(QtCore.Qt.blue))
                pivas_info.setText("🍺 Pivas mode deactivated 🍺")
                self.pivas = False
                self.lineEditDelay.setText("0")
            pivas_info.setIcon(QtWidgets.QMessageBox.Information)
            pivas_info.exec_()
            for i in range(self.buf_objX.size-1):
                self.bres_int(self.buf_objX[i], self.buf_objY[i], self.buf_objX[i + 1], self.buf_objY[i + 1])
            self.bres_int(self.buf_objX[0], self.buf_objY[0], self.buf_objX[self.buf_objX.size - 1], self.buf_objY[self.buf_objY.size - 1])
        elif int(press.key()) == QtCore.Qt.Key_Shift:
            if self.objX.size >= 3:
                self.bres_int(self.objX[0], self.objY[0], self.objX[self.objX.size - 1], self.objY[self.objY.size - 1])
            self.buf_objX = np.copy(self.objX)
            self.buf_objY = np.copy(self.objY)
            self.objX = np.array([], dtype=int)
            self.objY = np.array([], dtype=int)
        self.pm = self.pm.fromImage(self.img)
        self.label.setPixmap(self.pm)

    def close_fig(self):
        self.img = self.pm.toImage()
        if self.objX.size >= 3:
            self.bres_int(self.objX[0], self.objY[0], self.objX[self.objX.size - 1], self.objY[self.objY.size - 1])
        self.buf_objX = np.copy(self.objX)
        self.buf_objY = np.copy(self.objY)
        self.objX = np.array([], dtype=int)
        self.objY = np.array([], dtype=int)
        self.pm = self.pm.fromImage(self.img)
        self.label.setPixmap(self.pm)

    def wait(self):
        t = int(self.lineEditDelay.text())
        if t > 0:
            self.update_image()
        loop = QtCore.QEventLoop()
        QtCore.QTimer.singleShot(t, loop.quit)
        loop.exec_()

    def update_image(self):
        self.pm = self.pm.fromImage(self.img)
        self.label.setPixmap(self.pm)
        self.label.repaint()

    def pivas_sound(self):
        playsound("C:/msys64/home/BarDuck/ComGr/lab_06/Temp/pivas.mp3")

    def fill(self):
        if self.pivas:
            pivas_thread = threading.Thread(target=self.pivas_sound)
            pivas_thread.start()
        #  stack = [self.pixel_y, self.pixel_x]
        while len(self.stack) != 0:
            if self.pivas:
                num = rd.randint(0, len(self.stack) - 1)
                if num % 2 == 0:
                    num += 1
                p_x = self.stack.pop(num)
                p_y = self.stack.pop(num-1)
            else:
                p_x = self.stack.pop()
                p_y = self.stack.pop()
            x = p_x; y = p_y
            x_buff = x
            while self.img.pixelColor(x, y).rgb() != self.colour_edge.rgb():
                if x == 0:
                    return
                self.img.setPixel(x, y, self.colour_fill.rgb())
                x -= 1
            x_left = x + 1
            x = x_buff + 1
            while self.img.pixelColor(x, y).rgb() != self.colour_edge.rgb():
                self.img.setPixel(x, y, self.colour_fill.rgb())
                x += 1
            x_right = x - 1
            x = x_left; y += 1
            for i in range(0, 2):
                while x <= x_right:
                    flag = False
                    while self.img.pixelColor(x, y).rgb() != self.colour_edge.rgb() and \
                            self.img.pixelColor(x, y).rgb() != self.colour_fill.rgb() and \
                            x <= x_right:
                        flag = True
                        x += 1
                    if flag:
                        if self.img.pixelColor(x, y).rgb() != self.colour_edge.rgb() and \
                                self.img.pixelColor(x, y).rgb() != self.colour_fill.rgb() and \
                                x == x_right:
                            self.stack.append(y); self.stack.append(x)
                        else:
                            self.stack.append(y); self.stack.append(x - 1)
                    x_buff = x
                    while self.img.pixelColor(x, y).rgb() == self.colour_fill.rgb() and x < x_right:
                        x += 1
                    if x == x_buff:
                        x += 1
                y -= 2
                x = x_left
                self.wait()
            self.update_image()

    def count_time(self):
        start = time.time()
        self.fill()
        self.lineEditTime.setText(str(round(time.time() - start, 4)))
        self.lineEditTime.repaint()

    def clean_screen(self):
        self.pm.fill(self.white)
        self.img = self.pm.toImage()
        self.label.setPixmap(self.pm)
        self.label.repaint()
        self.buf_objX = np.copy(self.objX)
        self.buf_objY = np.copy(self.objY)
        self.objX = np.array([], dtype=int)
        self.objY = np.array([], dtype=int)
        self.stack = []

def sign(x):
    if x < 0:
        return -1
    elif x > 0:
        return 1
    return 0

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Visual()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
    