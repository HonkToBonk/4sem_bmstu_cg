import sys
import win
from math import pi, sin, cos, sqrt
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

wind = None

funcs = [
    lambda x, z: cos(x) * z / 3,
    lambda x, z: sin(cos(x)) * sin(z),
    lambda x, z: cos(sqrt(x**2 + z**2)),
    lambda x, z: sin(z) * cos(x),
    lambda x, z: cos(sin(x * z))
]

funcs_names = [
    "cos(x) * z / 3",
    "sin(cos(x)) * sin(z)",
    "cos(sqrt(x^2 + z^2))",
    "sin(z) * cos(x)",
    "cos(sin(x * z))"
]

class MainWindow(QtWidgets.QMainWindow, win.Ui_MainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)

        self.scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        self.w, self.h = 1170, 760

        self.scene.setSceneRect(0, 0, 1700, 1480)
        self.image = QImage(self.w, self.h, QImage.Format_RGB30)
        self.image.fill(Qt.white)
        self.pen_res = QtGui.QPen(QtCore.Qt.black)
        self.color_res = QtCore.Qt.black

        self.pen_res.setWidth(0)

        self.scale_k = 40
        self.k_coef.setValue(self.scale_k)

        self.x_begin = -10
        self.inp_x_from.setValue(self.x_begin)
        self.x_end = 10
        self.inp_x_to.setValue(self.x_end)
        self.x_step = 0.1
        self.inp_x_step.setValue(self.x_step)

        self.z_begin = -10
        self.inp_z_from.setValue(self.z_begin)
        self.z_end = 10
        self.inp_z_to.setValue(self.z_end)
        self.z_step = 0.1
        self.inp_z_step.setValue(self.z_step)

        self.alpha_x = 0
        self.angle_x.setValue(20)
        self.alpha_y = 0
        self.angle_y.setValue(20)
        self.alpha_z = 0
        self.angle_z.setValue(20)

        self.color_back = QtCore.Qt.white
        self.pen_res.setColor(QtCore.Qt.black)
        self.color_res = QtCore.Qt.black
        self.flag_scale_or_not = False

        for i in funcs_names:
            self.func_choose.addItem(i)

        self.use_k_coef.clicked.connect(self.scale)
        self.rotate_x.clicked.connect(self.turn_x)
        self.rotate_y.clicked.connect(self.turn_y)
        self.rotate_z.clicked.connect(self.turn_z)
        self.clear_scr.clicked.connect(self.clean_screen)
        self.draw.clicked.connect(self.draw_res)

    def clean_screen(self):
        self.scene.clear()
        self.trans_matrix = [[int(i == j) for i in range(4)] for j in range(4)]
        self.flag_scale_or_not = False
        self.alpha_x = 0
        self.alpha_y = 0
        self.alpha_z = 0

    # Поворот вокруг Х
    def turn_x(self):
        self.alpha_x += self.angle_x.value()
        self.draw_res()

    # Поворот вокруг У
    def turn_y(self):
        self.alpha_y += self.angle_y.value()
        self.draw_res()

    # Поворот вокруг Z
    def turn_z(self):
        self.alpha_z += self.angle_z.value()
        self.draw_res()

    # Масштабирование
    def scale(self):
        self.scale_k = self.k_coef.value()
        self.flag_scale_or_not = True
        self.draw_res()

    # Чтение значений начала конца и шага по осям X и Z
    def read_x_z_value(self):
        x_b = self.inp_x_from.value()
        x_e = self.inp_x_to.value()
        x_s = self.inp_x_step.value()

        z_b = self.inp_z_from.value()
        z_e = self.inp_z_to.value()
        z_s = self.inp_z_step.value()

        if not self.flag_scale_or_not:
            f = funcs[self.func_choose.currentIndex()]
            y2 = max(f(x_b, z_b), f(x_b, z_e), f(x_e, z_b), f(x_e, z_e))
            y1 = min(f(x_b, z_b), f(x_b, z_e), f(x_e, z_b), f(x_e, z_e))

            if abs(y2 - y1) < 1e-6:
                k1 = 45
            else:
                k1 = int(self.h / (y2 - y1)) - 1

            k2 = int(self.w / (x_e - x_b)) - 1

            self.scale_k = min(k1, k2)

        self.x_begin = int(x_b)
        self.x_end = int(x_e)
        self.x_step = x_s

        self.z_begin = int(z_b)
        self.z_end = int(z_e)
        self.z_step = z_s

    def draw_res(self):
        self.scene.clear()
        self.image.fill(QtCore.Qt.white)

        self.read_x_z_value()

        self.image = self.float_horizon()

        p = QPixmap()
        p.convertFromImage(self.image)
        self.scene.addPixmap(p)

    def float_horizon(self):
        # для удобства использования
        func = funcs[self.func_choose.currentIndex()]

        alpha_x, alpha_y, alpha_z = self.alpha_x, self.alpha_y, self.alpha_z
        x_min, x_max, x_step = self.x_begin, self.x_end, self.x_step
        z_min, z_max, z_step = self.z_begin, self.z_end, self.z_step

        # инициализация для боковых ребер
        x_r, y_r, x_l, y_l = -1, -1, -1, -1

        # инициализация массивов горизонта
        hight_hor = {x: 0 for x in range(0, int(self.w) + 1)}
        low_hor = {x: self.h for x in range(0, int(self.w) + 1)}

        z = z_max

        while z >= z_min:
            z_buf = z
            x_prev = x_min
            y_prev = func(x_min, z)
            x_prev, y_prev, z_buf = transform(x_prev, y_prev, z, alpha_x, alpha_y, alpha_z, self.scale_k, self.w, self.h)

            if x_l != -1:
                hight_hor, low_hor = horizon(x_prev, y_prev, x_l, y_l, hight_hor, low_hor, self.image)
            x_l = x_prev
            y_l = y_prev

            x = x_min
            while x <= x_max:
                y = func(x, z)
                x_cur, y_cur, z_buf = transform(x, y, z, alpha_x, alpha_y, alpha_z, self.scale_k, self.w, self.h)
                hight_hor, low_hor = horizon(x_prev, y_prev, x_cur, y_cur, hight_hor, low_hor, self.image)
                x_prev = x_cur
                y_prev = y_cur
                x += x_step

            if z != z_max:
                x_r, y_r = x_max, func(x_max, z - z_step)
                x_r, y_r, z_buf = transform(x_r, y_r, z - z_step, alpha_x, alpha_y, alpha_z, self.scale_k, self.w, self.h)
                hight_hor, low_hor = horizon(x_prev, y_prev, x_r, y_r, hight_hor, low_hor, self.image)
            z -= z_step

        return self.image

def sign(x):
    if not x:
        return 0
    return x / abs(x)

def is_visible(point):
    return 0 <= point[0] < wind.w - 1 and 0 <= point[1] < wind.h - 1

def horizon(x1, y1, x2, y2, hh, lh, image):
    if x1 < 0 or x1 > image.width() or x2 < 0 or x2 > image.width():
        return hh, lh

    x, y = x1, y1
    dx, dy = x2 - x1, y2 - y1
    s_x, s_y = sign(dx), sign(dy)
    dx, dy = abs(dx), abs(dy)

    if dx == 0 and dy == 0 and 0 <= x < image.width():
        if y >= hh[x]:
            hh[x] = y
            image.setPixelColor(x, image.height() - y, wind.color_res)
        if y <= lh[x]:
            lh[x] = y
            image.setPixelColor(x, image.height() - y, wind.color_res)
        return hh, lh
    flag = 0
    if dy > dx:
        dx, dy = dy, dx
        flag = 1

    y_max_cur, y_min_cur = hh[x], lh[x]

    e = 2 * dy - dx
    i = 1
    while i <= dx:
        if 0 <= x < image.width():
            if y >= hh[x]:
                if y >= y_max_cur:
                    y_max_cur = y
                image.setPixelColor(int(x), int(image.height() - y), wind.color_res)
            if y <= lh[x]:
                if y <= y_min_cur:
                    y_min_cur = y
                image.setPixelColor(int(x), int(image.height() - y), wind.color_res)
        if e >= 0:
            if not flag:
                y += s_y
            else:
                hh[x] = y_max_cur
                lh[x] = y_min_cur
                x += s_x
                y_max_cur = hh[x]
                y_min_cur = lh[x]
            e -= 2 * dx
        if e < 0:
            if flag:
                y += s_y
            else:
                hh[x] = y_max_cur
                lh[x] = y_min_cur
                x += s_x
                y_max_cur = hh[x]
                y_min_cur = lh[x]
            e += 2 * dy
        i += 1
    return hh, lh

def turn_x(x, y, z, alpha):
    alpha = alpha * pi / 180
    buf = y
    y = cos(alpha) * y - sin(alpha) * z
    z = cos(alpha) * z + sin(alpha) * buf
    return x, y, z

def turn_y(x, y, z, alpha):
    alpha = alpha * pi / 180
    buf = x
    x = cos(alpha) * x - sin(alpha) * z
    z = cos(alpha) * z + sin(alpha) * buf
    return x, y, z

def turn_z(x, y, z, alpha):
    alpha = alpha * pi / 180
    buf = x
    x = cos(alpha) * x - sin(alpha) * y
    y = cos(alpha) * y + sin(alpha) * buf
    return x, y, z

def transform(x, y, z, alpha_x, alpha_y, alpha_z, scale_k, w, h):
    x, y, z = turn_x(x, y, z, alpha_x)
    x, y, z = turn_y(x, y, z, alpha_y)
    x, y, z = turn_z(x, y, z, alpha_z)
    x = x * scale_k + w / 2
    y = y * scale_k + h / 2
    return round(x), round(y), round(z)

def main():
    global wind
    app = QtWidgets.QApplication(sys.argv)
    wind = MainWindow()
    wind.show()
    app.exec_()

if __name__ == "__main__":
    main()
