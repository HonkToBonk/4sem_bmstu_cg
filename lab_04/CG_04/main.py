import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import design
from numpy import arange
from time import time
from math import pi, cos, sin, sqrt
import matplotlib.pyplot as plt


class Visual(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.graphicsView.scale(0.5, -0.5)
        self.scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        h = self.graphicsView.height()
        w = self.graphicsView.width()
        self.scene.setSceneRect(-w/2, -h/2, w-2, h-2)
        self.pen = QtGui.QPen(QtCore.Qt.black)
        self.pen.setWidth(0)

        # Связи кнопок и функций.
        self.pushButtonScreenClean.clicked.connect(self.clean_screen)
        self.radioButtonBlack.clicked.connect(self.set_black)
        self.radioButtonWhite.clicked.connect(self.set_white)
        self.pushButtonDrawCircle.clicked.connect(self.circle)
        self.pushButtonDrawEll.clicked.connect(self.ellipse)
        self.pushButtonDrawSpecCirc.clicked.connect(self.spec_circle)
        self.pushButtonDrawSpecEll.clicked.connect(self.spec_ellipse)
        self.pushButtonTimeComp.clicked.connect(self.time_compare)

    def clean_screen(self):
        self.scene.clear()

    def set_black(self):
        self.pen.setColor(QtCore.Qt.black)

    def set_white(self):
        self.pen.setColor(QtCore.Qt.white)

    def circle(self):
        x_center = int(self.lineEditStartX.text())
        y_center = int(self. lineEditStartY.text())
        radius = int(self.lineEditR.text())
        self.draw_circle(x_center, y_center, radius)

    def spec_circle(self):
        x_center = int(self.lineEditStartX.text())
        y_center = int(self.lineEditStartY.text())
        r_start = int(self.lineEditStartR.text())
        step = int(self.lineEditStepR.text())
        count = int(self.lineEditCount.text())
        for i in range(0, count):
            self.draw_circle(x_center, y_center, r_start)
            r_start += step

    def spec_circle_time(self, draw):
        x_center = int(self.lineEditStartX.text())
        y_center = int(self.lineEditStartY.text())
        r_start = int(self.lineEditStartR.text())
        step = int(self.lineEditStepR.text())
        count = int(self.lineEditCount.text())
        for i in range(0, count):
            self.draw_circle(x_center, y_center, r_start, draw)
            r_start += step

    def ellipse(self):
        x_center = int(self.lineEditStartXEll.text())
        y_center = int(self.lineEditStartYEll.text())
        a = int(self.lineEditWidth.text())
        b = int(self.lineEditHeight.text())
        self.draw_ellipse(x_center, y_center, a, b)

    def spec_ellipse(self):
        x_center = int(self.lineEditStartXEll.text())
        y_center = int(self.lineEditStartYEll.text())
        a = int(self.lineEditStartWidth.text())
        b = int(self.lineEditStartHeight.text())
        step = int(self.lineEditStepEll.text())
        count = int(self.lineEditCountEll.text())
        for i in range(0, count):
            self.draw_ellipse(x_center, y_center, a, b)
            a += step
            b += step

    def draw_circle(self, x_center, y_center, radius, draw=True):
        if self.radioButtonParamYr.isChecked():
            self.paramCircle(x_center, y_center, radius, draw)
        elif self.radioButtonKanonYr.isChecked():
            self.canonCircle(x_center, y_center, radius, draw)
        elif self.radioButtonBres.isChecked():
            self.bresCircle(x_center, y_center, radius, draw)
        elif self.radioButtonSredToch.isChecked():
            self.midPointCircle(x_center, y_center, radius, draw)
        elif self.radioButtonLib.isChecked():
            self.scene.addEllipse(x_center - radius, y_center - radius, radius * 2, radius * 2, self.pen)

    def draw_ellipse(self, x_centre, y_centre, a, b):
        if self.radioButtonParamYr.isChecked():
            self.paramEllipse(x_centre, y_centre, a, b)
        elif self.radioButtonKanonYr.isChecked():
            self.canonEllipse(x_centre, y_centre, a, b)
        elif self.radioButtonBres.isChecked():
            self.canonEllipse(x_centre, y_centre, a, b)
        elif self.radioButtonSredToch.isChecked():
            self.midPointEllipse(x_centre, y_centre, a, b)
        elif self.radioButtonLib.isChecked():
            self.scene.addEllipse(x_centre - a, y_centre - b, a * 2, b * 2, self.pen)

    def draw_pixel(self, x, y):
        self.scene.addLine(x, y, x, y, self.pen)

    # Алгоритм построения окружности (Паметрическое ур.)
    def paramCircle(self, x_center, y_center, radius, draw=True):
        step = 1 / radius
        for t in arange(0, pi / 4 + step, step):
            x = round(radius * cos(t))
            y = round(radius * sin(t))
            if draw:
                self.draw_pixel(x_center + x, y_center + y)
                self.draw_pixel(x_center + x, y_center - y)
                self.draw_pixel(x_center - x, y_center + y)
                self.draw_pixel(x_center - x, y_center - y)
                self.draw_pixel(x_center + y, y_center + x)
                self.draw_pixel(x_center + y, y_center - x)
                self.draw_pixel(x_center - y, y_center + x)
                self.draw_pixel(x_center - y, y_center - x)

    # Алгоритм построения эллипса (Паметрическое ур.)
    def paramEllipse(self, x_center, y_center, a, b):
        if a > b:
            step = 1 / a
        else:
            step = 1 / b
        for t in arange(0, pi / 2 + step, step):
            x = round(a * cos(t))
            y = round(b * sin(t))
            self.draw_pixel(x_center + x, y_center + y)
            self.draw_pixel(x_center + x, y_center - y)
            self.draw_pixel(x_center - x, y_center + y)
            self.draw_pixel(x_center - x, y_center - y)

    # Алгоритм построения окружности (Каноническое ур.)
    def canonCircle(self, x_center, y_center, radius, draw=True):
        limit = round(radius / sqrt(2))
        radius_pow = radius * radius
        for x in range(0, limit + 1):
            y = round(sqrt(radius_pow - x * x))
            if draw:
                self.draw_pixel(x_center + x, y_center + y)
                self.draw_pixel(x_center + x, y_center - y)
                self.draw_pixel(x_center - x, y_center + y)
                self.draw_pixel(x_center - x, y_center - y)
                self.draw_pixel(x_center + y, y_center + x)
                self.draw_pixel(x_center + y, y_center - x)
                self.draw_pixel(x_center - y, y_center + x)
                self.draw_pixel(x_center - y, y_center - x)

    # Алгоритм построения эллипса (Каноническое ур.)
    def canonEllipse(self, x_center, y_center, a, b):
        a_pow = a * a
        b_pow = b * b
        limit = round(a_pow / sqrt(a_pow + b_pow))
        for x in range(0, limit + 1):
            y = round(sqrt(1 - x * x / a_pow) * b)
            self.draw_pixel(x_center + x, y_center + y)
            self.draw_pixel(x_center + x, y_center - y)
            self.draw_pixel(x_center - x, y_center + y)
            self.draw_pixel(x_center - x, y_center - y)
        limit = round(b_pow / sqrt(a_pow + b_pow))
        for y in range(limit, -1, -1):
            x = round(sqrt(1 - y * y / b_pow) * a)
            self.draw_pixel(x_center + x, y_center + y)
            self.draw_pixel(x_center + x, y_center - y)
            self.draw_pixel(x_center - x, y_center + y)
            self.draw_pixel(x_center - x, y_center - y)

    # Алгоритм построения окружности (алгоритм Брезенхема)
    def bresCircle(self, x_center, y_center, radius, draw=True):
        x = 0
        y = radius
        d = 2 * (1 - radius)
        eps = 0
        while x <= y:
            if draw:
                self.draw_pixel(x_center + x, y_center + y)
                self.draw_pixel(x_center + x, y_center - y)
                self.draw_pixel(x_center - x, y_center + y)
                self.draw_pixel(x_center - x, y_center - y)
                self.draw_pixel(x_center + y, y_center + x)
                self.draw_pixel(x_center + y, y_center - x)
                self.draw_pixel(x_center - y, y_center + x)
                self.draw_pixel(x_center - y, y_center - x)
            if d <= 0:
                eps = 2 * d + 2 * y - 1
                if eps < 0:
                    param = 1
                else:
                    param = 2
            elif d > 0:
                eps = 2 * d - 2 * x - 1
                if eps < 0:
                    param = 2
                else:
                    param = 3
            if param == 1:
                x += + 1
                d += 2 * x + 1
            elif param == 2:
                x += + 1
                y -= 1
                d += 2 * x - 2 * y + 2
            else:
                y -= 1
                d -= 2 * y + 1

    # Алгоритм построения эллипса (алгоритм Брезенхема)
    def bresEllipse(self, x_center, y_center, a, b):
        x = 0
        y = b
        a_pow = a * a
        b_pow = b * b
        d = b ** 2 - a_pow * (2 * b + 1)
        while y > 0:
            self.draw_pixel(x_center + x, y_center + y)
            self.draw_pixel(x_center + x, y_center - y)
            self.draw_pixel(x_center - x, y_center + y)
            self.draw_pixel(x_center - x, y_center - y)
            if d <= 0:
                d1 = 2 * d + a_pow * (2 * y - 1)
                x += 1
                d += b_pow * (2 * x + 1)
                if d1 >= 0:
                    y -= 1
                    d += a_pow * (-2 * y + 1)
            else:
                d1 = 2 * d + b_pow * (-2 * x - 1)
                y -= 1
                d += a_pow * (-2 * y + 1)
                if d1 < 0:
                    x += 1
                    d += b_pow * (2 * x + 1)

    # Алгоритм построения окружности (алгоритм средней точки)
    def midPointCircle(self, x_center, y_center, radius, draw=True):
        x = 0
        y = radius
        d = 1 - radius
        while x <= y:
            if draw:
                self.draw_pixel(x_center + x, y_center + y)
                self.draw_pixel(x_center + x, y_center - y)
                self.draw_pixel(x_center - x, y_center + y)
                self.draw_pixel(x_center - x, y_center - y)
                self.draw_pixel(x_center + y, y_center + x)
                self.draw_pixel(x_center + y, y_center - x)
                self.draw_pixel(x_center - y, y_center + x)
                self.draw_pixel(x_center - y, y_center - x)
            x += 1
            if d < 0:
                d += 2 * x + 1
            else:
                y -= 1
                d += 2 * (x - y) + 1

    # Алгоритм построения эллипса (алгоритм средней точки)
    def midPointEllipse(self, x_center, y_center, a, b):
        x = 0
        y = b
        a_pow = a * a
        b_pow = b * b
        delta = b_pow - a_pow * b + 0.25 * a * b
        dx = 2 * b_pow * x
        dy = 2 * a_pow * y
        while dx < dy:
            self.draw_pixel(x_center + x, y_center + y)
            self.draw_pixel(x_center + x, y_center - y)
            self.draw_pixel(x_center - x, y_center + y)
            self.draw_pixel(x_center - x, y_center - y)
            x += 1
            dx += 2 * b_pow
            if delta >= 0:
                y -= 1
                dy -= 2 * a_pow
                delta -= dy
            delta += dx + b_pow
        delta = b_pow * (x + 0.5) ** 2 + a_pow * (y - 1) ** 2 - a_pow * b_pow
        while y >= 0:
            self.draw_pixel(x_center + x, y_center + y)
            self.draw_pixel(x_center + x, y_center - y)
            self.draw_pixel(x_center - x, y_center + y)
            self.draw_pixel(x_center - x, y_center - y)
            y -= 1
            dy -= 2 * a_pow
            if delta <= 0:
                x += 1
                dx += 2 * b_pow
                delta += dx
            delta -= dy - a_pow

    def time_compare(self):
        self.lineEditStartR.setText('10')
        self.lineEditStepR.setText('10')
        self.lineEditCount.setText('10')
        data = []

        self.radioButtonKanonYr.toggle()
        start = time()
        for i in range(100):
            self.spec_circle_time(False)
        data.append(time() - start)
        self.radioButtonParamYr.toggle()
        start = time()
        for i in range(100):
            self.spec_circle_time(False)
        data.append(time() - start)
        self.radioButtonBres.toggle()
        start = time()
        for i in range(100):
            self.spec_circle_time(False)
        data.append(time() - start)
        self.radioButtonSredToch.toggle()
        start = time()
        for i in range(100):
            self.spec_circle_time(False)
        data.append(time() - start)
        self.radioButtonLib.toggle()
        start = time()
        for i in range(100):
            self.spec_circle()
        data.append(time() - start)
        self.radioButtonKanonYr.toggle()
        self.lineEditStartR.setText('0')
        self.lineEditStepR.setText('0')
        self.lineEditCount.setText('0')
        self.scene.clear()
        fig, ax = plt.subplots()
        ax.bar(['Канонич-е \nур-е', 'Параметрич-е \nур-е', 'Брезенхем', 'Средняя \nточка', 'Библиот-я \nф-я'], data, color='green')
        ax.set_facecolor('seashell')
        plt.title("Исследование временных характеристик")
        plt.ylabel("Время работы в секундах")
        plt.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Visual()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
