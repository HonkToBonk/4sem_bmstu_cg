import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import design
from math import fabs

class Visual(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.label.setPalette(QtGui.QPalette(QtCore.Qt.white))
        self.white = QtGui.QColor(QtCore.Qt.white)

        self.colour_cutter = QtGui.QColor(QtCore.Qt.black)
        self.colour_line_out = QtGui.QColor(QtCore.Qt.red)
        self.colour_line_in = QtGui.QColor(QtCore.Qt.blue)

        self.labelColourCutter.setPalette(QtGui.QPalette(QtCore.Qt.black))
        self.labelColourLineOut.setPalette(QtGui.QPalette(QtCore.Qt.red))
        self.labelColourLineIn.setPalette(QtGui.QPalette(QtCore.Qt.blue))

        self.pm = QtGui.QPixmap(820, 730)
        self.pm.fill(self.white)
        self.img = self.pm.toImage()

        self.p_x = []
        self.p_y = []
        self.cutter_x = []
        self.cutter_y = []
        self.cutter_closed = False

        self.pushButtonScreenClean.clicked.connect(self.clean_screen)
        self.pushButtonProc.clicked.connect(self.proc)
        self.pushButtonCutterClosed.clicked.connect(self.close_cutter)

    def draw_point(self, x, y, colour):
        # Пиксель
        self.img.setPixel(x, y, colour.rgb())
        # Вокруг пикселя
        self.img.setPixel(x-1, y, colour.rgb())
        self.img.setPixel(x+1, y, colour.rgb())
        self.img.setPixel(x, y-1, colour.rgb())
        self.img.setPixel(x, y+1, colour.rgb())
        # Диагональные вокруг пикселя
        self.img.setPixel(x-1, y-1, colour.rgb())
        self.img.setPixel(x-1, y+1, colour.rgb())
        self.img.setPixel(x+1, y-1, colour.rgb())
        self.img.setPixel(x+1, y+1, colour.rgb())
        # Дополнительные
        self.img.setPixel(x-2, y, colour.rgb())
        self.img.setPixel(x+2, y, colour.rgb())
        self.img.setPixel(x, y-2, colour.rgb())
        self.img.setPixel(x, y+2, colour.rgb())

    def bres_int(self, x_start, y_start, x_end, y_end, colour):
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
            self.img.setPixel(x, y, colour.rgb())
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

    def mousePressEvent(self, press):
        if press.pos().x() < self.label.pos().x() or press.pos().y() < self.label.pos().y():
            return
        self.img = self.pm.toImage()
        if press.button() == QtCore.Qt.LeftButton:
            if self.verticalMode.isChecked() and len(self.p_x) % 2 == 1:
                self.p_x.append(self.p_x[len(self.p_x) - 1])
                self.p_y.append((press.pos() - self.label.pos()).y())
            elif self.horizontalMode.isChecked() and len(self.p_x) % 2 == 1:
                self.p_x.append((press.pos() - self.label.pos()).x())
                self.p_y.append(self.p_y[len(self.p_y) - 1])
            else:
                self.p_x.append((press.pos() - self.label.pos()).x())
                self.p_y.append((press.pos() - self.label.pos()).y())
            self.draw_point(self.p_x[len(self.p_x) - 1], self.p_y[len(self.p_y) - 1], self.colour_line_out)
            if len(self.p_x) % 2 == 0:
                self.bres_int(self.p_x[len(self.p_x) - 2], self.p_y[len(self.p_y) - 2],
                              self.p_x[len(self.p_x) - 1], self.p_y[len(self.p_y) - 1], self.colour_line_out)
        elif press.button() == QtCore.Qt.RightButton:
            if self.cutter_closed:
                return
            self.cutter_x.append((press.pos() - self.label.pos()).x())
            self.cutter_y.append((press.pos() - self.label.pos()).y())
            if len(self.cutter_x) > 1 and self.cutter_x[len(self.cutter_x) - 1] == self.cutter_x[len(self.cutter_x) - 2] and \
                        self.cutter_y[len(self.cutter_y) - 1] == self.cutter_y[len(self.cutter_y) - 2]:
                    self.cutter_x.pop()
                    self.cutter_y.pop()
            self.draw_point(self.cutter_x[len(self.cutter_x) - 1], self.cutter_y[len(self.cutter_y) - 1], self.colour_cutter)
            if len(self.cutter_x) > 1:
                self.bres_int(self.cutter_x[len(self.cutter_x) - 2], self.cutter_y[len(self.cutter_y) - 2],
                              self.cutter_x[len(self.cutter_x) - 1], self.cutter_y[len(self.cutter_y) - 1],
                              self.colour_cutter)
        self.pm = self.pm.fromImage(self.img)
        self.label.setPixmap(self.pm)

    def close_cutter(self):
        if len(self.cutter_x) < 3:
            self.show_error(3)
        if self.cutter_closed:
            return
        self.cutter_closed = True
        self.img = self.pm.toImage()
        self.bres_int(self.cutter_x[0], self.cutter_y[0], self.cutter_x[len(self.cutter_x) - 1],
                      self.cutter_y[len(self.cutter_y) - 1], self.colour_cutter)
        self.pm = self.pm.fromImage(self.img)
        self.label.setPixmap(self.pm)

    def count_product(self, first, second, third):
        ab_x = self.cutter_x[second] - self.cutter_x[first]
        ab_y = self.cutter_y[second] - self.cutter_y[first]
        bc_x = self.cutter_x[third] - self.cutter_x[second]
        bc_y = self.cutter_y[third] - self.cutter_y[second]
        prod = ab_x * bc_y - ab_y * bc_x
        return prod

    def check_cutter(self):
        flag_right = True
        flag_left = True
        for i in range(1, len(self.cutter_x)):
            if i == len(self.cutter_x) - 1:
                product = self.count_product(i - 1, i, 0)
            else:
                product = self.count_product(i - 1, i, i + 1)
            if not product < 0:
                flag_left = False
                break
        for i in range(len(self.cutter_x) - 1, 0, -1):
            if i == len(self.cutter_x) - 1:
                product = self.count_product(i - 1, i, 0)
            else:
                product = self.count_product(i - 1, i, i + 1)
            if not product > 0:
                flag_right = False
                break
        return flag_left or flag_right

    def show_error(self, mode):
        error = QtWidgets.QMessageBox()
        error.setWindowTitle("Ошибка")
        if mode == 0:
            error.setText("Отсекатель невыпуклый!\nПовторите ввод!")
        elif mode == 1:
            error.setText("Недостаточно отрезков для отсечения!\nВведите хотя бы один!")
        elif mode == 2:
            error.setText("Отсекатель не замкнут!\nЗамкните отсекатель!")
        elif mode == 3:
            error.setText("Отсекатель не замкнут!\nНедостаточно вершин для замыкания!")
        else:
            error.setText("Произошла неизвестная ошибка!\nВ другой раз повезет больше!")
        error.setIcon(QtWidgets.QMessageBox.Warning)
        error.exec_()

    def proc(self):
        if len(self.cutter_x) < 3:
            self.show_error(3)
            return
        if not self.cutter_closed:
            self.show_error(2)
            return
        if len(self.p_x) < 2:
            self.show_error(1)
            return
        if not self.check_cutter():
            self.clean_screen()
            self.show_error(0)
            return
        self.img = self.pm.toImage()
        obh = -1
        xv1 = self.cutter_x[1] - self.cutter_x[0]
        yv1 = self.cutter_y[1] - self.cutter_y[0]
        xv2 = self.cutter_x[2] - self.cutter_x[1]
        yv2 = self.cutter_y[2] - self.cutter_y[1]
        if xv1 * yv2 - yv1 * xv2 > 0:
            obh = 1
        for i in range(0, len(self.p_x), 2):
            self.makeCut(self.p_x[i], self.p_y[i], self.p_x[i + 1], self.p_y[i + 1], obh)
        self.pm = self.pm.fromImage(self.img)
        self.label.setPixmap(self.pm)
        self.label.repaint()

    def makeCut(self, p1_x, p1_y, p2_x, p2_y, obh):
        t_begin = 0
        t_end = 1
        d_x = p2_x - p1_x
        d_y = p2_y - p1_y
        for i in range(0, len(self.cutter_x)):
            w_x = p1_x - self.cutter_x[i]
            w_y = p1_y - self.cutter_y[i]
            n_x = (-self.cutter_y[(i + 1) % len(self.cutter_y)] + self.cutter_y[i]) * obh
            n_y = (self.cutter_x[(i + 1) % len(self.cutter_x)] - self.cutter_x[i]) * obh
            Wsc = w_x * n_x + w_y * n_y
            Dsc = d_x * n_x + d_y * n_y
            if Dsc == 0:
                if Wsc < 0:
                    return
                else:
                    continue
            t = - Wsc / Dsc
            if Dsc > 0:
                if t > 1:
                    return
                else:
                    t_begin = max(t, t_begin)
            if Dsc <= 0:
                if t < 0:
                    return
                else:
                    t_end = min(t, t_end)
            if t_begin > t_end:
                break

        if t_begin <= t_end:
            self.bres_int(p1_x + (p2_x - p1_x) * t_end, p1_y + (p2_y - p1_y) * t_end,
                          p1_x + (p2_x - p1_x) * t_begin, p1_y + (p2_y - p1_y) * t_begin, self.colour_line_in)
            self.draw_point(p1_x + (p2_x - p1_x) * t_end, p1_y + (p2_y - p1_y) * t_end, self.colour_line_in)
            self.draw_point(p1_x + (p2_x - p1_x) * t_begin, p1_y + (p2_y - p1_y) * t_begin, self.colour_line_in)
        return

    def clean_screen(self):
        self.pm.fill(self.white)
        self.img = self.pm.toImage()
        self.label.setPixmap(self.pm)
        self.label.repaint()
        self.p_x = []
        self.p_y = []
        self.cutter_x = []
        self.cutter_y = []
        self.cutter_closed = False

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

    # Как было раньше - не обрабатывается последнее ребро (замцкающее)
    # def check_cutter(self):
    #     flag_right = True
    #     flag_left = True
    #     for i in range(1, len(self.cutter_x) - 1):
    #         print(i)
    #         ab_x = self.cutter_x[i] - self.cutter_x[i - 1]
    #         ab_y = self.cutter_y[i] - self.cutter_y[i - 1]
    #         bc_x = self.cutter_x[i + 1] - self.cutter_x[i]
    #         bc_y = self.cutter_y[i + 1] - self.cutter_y[i]
    #         product = ab_x * bc_y - ab_y * bc_x
    #         if not product < 0:
    #             flag_left = False
    #             break
    #     for i in range(len(self.cutter_x) - 2, 0, -1):
    #         print(i)
    #         ab_x = self.cutter_x[i] - self.cutter_x[i - 1]
    #         ab_y = self.cutter_y[i] - self.cutter_y[i - 1]
    #         bc_x = self.cutter_x[i + 1] - self.cutter_x[i]
    #         bc_y = self.cutter_y[i + 1] - self.cutter_y[i]
    #         product = ab_x * bc_y - ab_y * bc_x
    #         if not product > 0:
    #             flag_right = False
    #             break
    #     print(flag_left)
    #     print(flag_right)
    #     return flag_left or flag_right
