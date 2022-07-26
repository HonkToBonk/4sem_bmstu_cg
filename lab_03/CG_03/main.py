import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import design
from time import time
from math import pi, cos, sin, radians, fabs, floor
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
        self.pushButtonDrawLine.clicked.connect(self.draw_line)
        self.pushButtonDrawSpectrum.clicked.connect(self.draw_spectrum)
        self.pushButtonTimeComp.clicked.connect(self.time_compare)
        self.pushButtonStepComp.clicked.connect(self.step_comp)

    def clean_screen(self):
        self.scene.clear()

    def set_black(self):
        self.pen.setColor(QtCore.Qt.black)

    def set_green(self):
        self.pen.setColor(QtCore.Qt.green)

    def set_white(self):
        self.pen.setColor(QtCore.Qt.white)

    def set_blue(self):
        self.pen.setColor(QtCore.Qt.blue)

    def add_line(self, x_start, y_start, x_end, y_end, draw=True):
        if self.radioButtonCDA.isChecked():
            self.cda(x_start, y_start, x_end, y_end, draw)
        elif self.radioButtonBresFloat.isChecked():
            self.bres_float(x_start, y_start, x_end, y_end, draw)
        elif self.radioButtonBresInt.isChecked():
            self.bres_int(x_start, y_start, x_end, y_end, draw)
        elif self.radioButtonBresSmooth.isChecked():
            self.bres_smooth(x_start, y_start, x_end, y_end, draw)
        elif self.radioButtonWu.isChecked():
            self.wu(x_start, y_start, x_end, y_end, draw)
        else:
            self.lib_func(x_start, y_start, x_end, y_end)

    def draw_line(self):
        try:
            x_start = float(self.lineEditStartX.text())
            y_start = float(self.lineEditStartX.text())
            x_end = float(self.lineEditEndX.text())
            y_end = float(self.lineEditEndY.text())
        except:
            QtWidgets.QMessageBox.critical(self, "", "Координаты начала и конца отрезка должны быть целыми "
                                                     "или веществеными числами!")
            return
        self.add_line(x_start, y_start, x_end, y_end)

    def draw_spectrum(self, bo=False, draw=True, length=600):
        try:
            angle = int(self.lineEditAngle.text())
        except:
            QtWidgets.QMessageBox.critical(self, "", "Угол поворота должен быть целым числом!")
            return
        if angle < 1:
            QtWidgets.QMessageBox.critical(self, "", "Угол поворота должен быть больше нуля!")
            return
        t = 0
        while t < 2 * pi - 0.001:
            x = length * cos(t)
            y = length * sin(t)
            self.add_line(0, 0, x, y, draw)
            t += radians(angle)

    def draw_pixel(self, x, y, alpha=255):
        color = self.pen.color()
        QtGui.QColor.setAlpha(color, alpha)
        self.pen.setColor(color)
        self.scene.addLine(x, y, x, y, self.pen)

    def lib_func(self, x_start, y_start, x_end, y_end):
        self.scene.addLine(round(x_start), round(y_start), round(x_end), round(y_end), self.pen)

    def cda(self, x_start, y_start, x_end, y_end, draw=True, steps=False):
        # Проверка вырожденности орезка в точку.
        if x_start == x_end and y_start == y_end and draw:
            self.draw_pixel(round(x_start), round(y_start))
            return
        # Вычисление длины отрезка.
        dx = x_end - x_start
        dy = y_end - y_start
        if fabs(dx) > fabs(dy):
            l = fabs(dx)
        else:
            l = fabs(dy)
        dx /= l
        dy /= l
        # Задание координатам текущей точки начальных значений.
        x = x_start
        y = y_start
        i = 1
        steps_num = 1
        while i <= l + 1:
            if draw:
                self.draw_pixel(round(x), round(y))
            if steps and i <= l:
                if not((round(x + dx) == round(x) and round(y + dy) != round(y)) or
                       (round(x + dx) != round(x) and round(y + dy) == round(y))):
                    steps_num += 1
            x += dx
            y += dy
            i += 1
        if steps:
            return steps_num

    def bres_float(self, x_start, y_start, x_end, y_end, draw=True, steps=False):
        # Проверка вырожденности орезка в точку.
        if x_start == x_end and y_start == y_end:
            if draw:
                self.draw_pixel(round(x_start), round(y_start))
            return
        # Вычисление приращений.
        dx = x_end - x_start
        dy = y_end - y_start
        # Вычисление шага изменения каждой координаты пиксела.
        sx = sign(dx)
        sy = sign(dy)
        # Вычисление модулей приращения координат.
        dx = fabs(dx)
        dy = fabs(dy)
        # Анализ вычисленного значения m и обмен местами dX и dY  при m > 1.
        if dy >= dx:
            dx, dy = dy, dx
            fl = 1  # флаг, определяющий факт обмена местами координат.
        else:
            fl = 0
        # Вычисление модуля тангенса угла наклона отрезка.
        m = dy / dx
        # Инициализация начального значения ошибки.
        f = m - 0.5
        # Инициализация начальных значений координат текущего пиксела.
        x = round(x_start)
        y = round(y_start)
        # Цикл от i=1 до i=dX+1 с шагом 1.
        i = 1
        steps_num = 1
        x_buff = x
        y_buff = y
        while i <= dx:
            # Высвечивание точки с координатами (X,Y).
            if draw:
                self.draw_pixel(x, y)
            # Вычисление координат и ошибки для следующего пиксела.
            if f >= 0:
                if fl == 1:
                    x += sx
                else:
                    y += sy
                f -= 1
            if f <= 0:
                if fl == 1:
                    y += sy
                else:
                    x += sx
                f += m
            i += 1
            if steps:
                if not((x_buff == x and y_buff != y) or (x_buff != x and y_buff == y)):
                    steps_num += 1
                x_buff = x
                y_buff = y
        if steps:
            return steps_num

    def bres_int(self, x_start, y_start, x_end, y_end, draw=True, steps=False):
        # Проверка вырожденности орезка в точку.
        if x_start == x_end and y_start == y_end:
            if draw:
                self.draw_pixel(round(x_start), round(y_start))
            return
        # Вычисление приращений.
        dx = x_end - x_start
        dy = y_end - y_start
        # Вычисление шага изменения каждой координаты пиксела.
        sx = sign(dx)
        sy = sign(dy)
        # Вычисление модулей приращения координат.
        dx = fabs(dx)
        dy = fabs(dy)
        # Анализ вычисленного значения m и обмен местами dX и dY  при m > 1.
        if dy >= dx:
            dx, dy = dy, dx
            fl = 1  # флаг, определяющий факт обмена местами координат.
        else:
            fl = 0
        # Инициализация начального значения ошибки.
        f = 2 * dy - dx
        # Инициализация начальных значений координат текущего пиксела.
        x = round(x_start)
        y = round(y_start)
        # Цикл от i=1 до i=dX+1 с шагом 1.
        i = 1
        steps_num = 1
        x_buff = x
        y_buff = y
        while i <= dx + 1:
            # Высвечивание точки с координатами (X,Y).
            if draw:
                self.draw_pixel(x, y)
            # Вычисление координат и ошибки для следующего пиксела.
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
            if steps:
                if not((x_buff == x and y_buff != y) or (x_buff != x and y_buff == y)):
                    steps_num += 1
                x_buff = x
                y_buff = y
        if steps:
            return steps_num

    def bres_smooth(self, x_start, y_start, x_end, y_end, draw=True, steps=False):
        I = 255
        # Проверка вырожденности отрезка.  Если отрезок  вырожден, то высвечивание отдельного пиксела.
        if x_start == x_end and y_start == y_end:
            if draw:
                self.draw_pixel(round(x_start), round(y_start))
            return
        # Вычисление приращений.
        dx = x_end - x_start
        dy = y_end - y_start
        # Вычисление шага изменения каждой координаты пиксела.
        sx = sign(dx)
        sy = sign(dy)
        # Вычисление модулей приращения координат.
        dx = fabs(dx)
        dy = fabs(dy)
        # Вычисление модуля тангенса угла наклона отрезка
        m = dy / dx
        # Анализ вычисленного значения m и обмен местами dX и dY при m > 1.
        if m >= 1:
            dx, dy = dy, dx
            m = 1 / m
            fl = 1  # флаг, определяющий факт обмена местами координат.
        else:
            fl = 0
        # Инициализация начального значения ошибки.
        f = I / 2
        # Инициализация начальных значений координат текущего пиксела.
        x = round(x_start)
        y = round(y_start)
        # Вычисление скорректированного  значения  тангенса  угла наклона m и коэффициента W.
        m *= I
        W = I - m
        # Высвечивание пиксела  с координатами  (X,Y) интенсивностью E(f).
        if draw:
            self.draw_pixel(x, y, round(f))
        steps_num = 1
        x_buff = x
        y_buff = y
        # Цикл от i=1 до i=dX с шагом 1.
        i = 1
        while i <= dx:
            if f < W:
                if fl == 0:
                    x += sx
                else:
                    y += sy
                f += m
            else:
                x += sx
                y += sy
                f -= W
            if draw:
                self.draw_pixel(x, y, round(f))
            if steps:
                if not((x == x_buff and y != y_buff) or (x != x_buff and y == y_buff)):
                    steps_num += 1
                x_buff = x
                y_buff = y
            i += 1
        if steps:
            return steps_num

    def wu(self, x_start, y_start, x_end, y_end, draw=True, steps=False):
        dx = x_end - x_start
        dy = y_end - y_start
        Imax = 255
        m = 1
        steps_num = 1
        if fabs(dy) > fabs(dx):
            if y_start > y_end:
                x_start, x_end = x_end, x_start
                y_start, y_end = y_end, y_start
            if dy != 0:
                m = dx / dy
            for y in range(round(y_start), round(y_end) + 1):
                d1 = x_start - floor(x_start)
                d2 = 1 - d1
                if draw:
                    # Нижняя точка.
                    self.draw_pixel(int(x_start), y, round(fabs(d2) * Imax))
                    # Верхняя точка.
                    self.draw_pixel(int(x_start) + 1, y, round(fabs(d1) * Imax))
                if steps and y < round(y_end):
                    if int(x_start) != int(x_start+m):
                        steps_num += 1
                x_start += m
        else:
            if x_start > x_end:
                x_start, x_end = x_end, x_start
                y_start, y_end = y_end, y_start
            if dx != 0:
                m = dy / dx
            for x in range(round(x_start), round(x_end) + 1):
                d1 = y_start - floor(y_start)
                d2 = 1 - d1
                if draw:
                    # Нижняя точка.
                    self.draw_pixel(x, int(y_start), round(fabs(d2) * Imax))
                    # Верхняя точка.
                    self.draw_pixel(x, int(y_start) + 1, round(fabs(d1) * Imax))
                if steps and x < round(x_end):
                    if int(y_start) != int(y_start+m):
                        steps_num += 1
                y_start += m
        if steps:
            return steps_num

    def time_compare(self):
        try:
            length = int(self.lineEditLineLen.text())
        except:
            QtWidgets.QMessageBox.critical(self, "", "Длина линии должна быть целым числом!")
            return
        if length < 1:
            QtWidgets.QMessageBox.critical(self, "", "Длина линии должна быть больше нуля!")
            return
        angle = self.lineEditAngle.text()
        self.lineEditAngle.setText('10')
        data = []

        self.radioButtonCDA.toggle()
        start = time()
        for i in range(5):
            self.draw_spectrum(draw=True, length=length)
        data.append(time() - start)
        self.radioButtonBresFloat.toggle()
        start = time()
        for i in range(5):
            self.draw_spectrum(draw=True, length=length)
        data.append(time() - start)
        self.radioButtonBresInt.toggle()
        start = time()
        for i in range(5):
            self.draw_spectrum(draw=True, length=length)
        data.append(time() - start)
        self.radioButtonBresSmooth.toggle()
        start = time()
        for i in range(5):
            self.draw_spectrum(draw=True, length=length)
        data.append(time() - start)
        self.radioButtonWu.toggle()
        start = time()
        for i in range(5):
            self.draw_spectrum(draw=True, length=length)
        data.append(time() - start)
        self.lineEditAngle.setText(angle)
        self.scene.clear()
        fig, ax = plt.subplots()
        ax.bar(['ЦДА', 'Брезенхем\n(float)', 'Брезенхем\n(int)', 'Брезенхем\nсглаживание', 'Ву'], data, color='green')
        ax.set_facecolor('seashell')
        plt.title("Исследование временных характеристик.")
        plt.ylabel("Время работы в секундах.")
        plt.show()

    def step_comp(self):
        try:
            length = int(self.lineEditLineLen.text()) - 1
        except:
            QtWidgets.QMessageBox.critical(self, "", "Длина линии должна быть целым числом!")
            return
        if length < 1:
            QtWidgets.QMessageBox.critical(self, "", "Длина линии должна быть больше нуля!")
            return
        cda = []
        bres_float = []
        bres_int = []
        bres_smooth = []
        wu = []

        t = 0
        angles = [i for i in range(0, 91, 2)]
        while t <= pi / 2 + 0.01:
            x = length * cos(t)
            y = length * sin(t)
            cda.append(self.cda(0, 0, x, y, False, True))
            bres_float.append(self.bres_float(0, 0, x, y, False, True))
            bres_int.append(self.bres_int(0, 0, x, y, False, True))
            bres_smooth.append(self.bres_smooth(0, 0, x, y, False, True))
            wu.append(self.wu(0, 0, x, y, False, True))
            t += radians(2)
        fig, ax = plt.subplots()
        # fig, ax = plt.subplots(2, 2)
        ax.plot(angles, cda, label='ЦДА')
        ax.plot(angles, bres_float, label='Брезенхем\n(float/int)')
        ax.plot(angles, bres_smooth, label='Брезенхем\nсглаживание')
        ax.plot(angles, wu, label='Ву')
        ax.set_facecolor('seashell')
        plt.title("Исследование ступенчатости.")
        plt.legend()
        plt.ylabel("Максимальное колличество ступенек.")
        plt.xlabel("Угол в градусах.")
        # ax[0, 0].plot(angles, cda)
        # ax[0, 0].set_title('ЦДА')
        # ax[0, 1].plot(angles, bres_float, 'tab:orange')
        # ax[0, 1].set_title('Брезенхем (float/int)')
        # ax[1, 0].plot(angles, bres_smooth, 'tab:green')
        # ax[1, 0].set_title('Брезенхем сглаживание')
        # ax[1, 1].plot(angles, wu, 'tab:red')
        # ax[1, 1].set_title('Ву')
        # for i in range(2):
        #     for j in range(2):
        #         ax[i, j].set(xlabel="Угол в градусах.", ylabel="Максимальное кол-во\nступенек.")
        # for i in range(2):
        #     for j in range(2):
        #         ax[i, j].label_outer()
        # plt.setp(ax, xticks=[i for i in range(0, 91, 10)], yticks=[i for i in range(8)])
        plt.show()

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
