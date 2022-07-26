import sys
from copy import deepcopy
from PyQt5 import QtWidgets, QtCore
from math import sin, cos, pi, radians, sqrt
import design

class Visual(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.graphicsView.scale(1, -1)
        self.arr_points = []  # Массив точек корпуса.
        self.arr_links = []  # Массив связей точек.
        self.arr_circle_centers = []  # Массив центров окружностей.
        self.arr_rads = []  # Массив содержащий радиусы окружностей.
        self.arr_circles_cords = []  # Массив, содержащий точки окружностей.

        # Массивы для возврата на один шаг назад.
        self.arr_points_buff = []
        self.arr_circle_centers_buff = []
        self.arr_rads_buff = []
        self.arr_circles_cords_buff = []
        self.start_scale = 4

        # Связи кнопок и функций.
        self.pushButton_draw_base.clicked.connect(self.draw_base)
        self.pushButton_back.clicked.connect(self.step_back)
        self.button_move.clicked.connect(self.move_func)
        self.button_scale.clicked.connect(self.scale_func)
        self.button_rotate.clicked.connect(self.rotate_func)

    # Вычисление начальных координат фигуры.
    def init_base_data(self):
        self.arr_points = [[10, 0], [10, 2], [23, 2], [23, 7], [8, 12], [4, 12], [0, 16], [-7, 16], [-11, 12], [-25, 7],
                           [-30, 7], [-30, 6], [-60, 6], [-60, 5], [-30, 5], [-30, 4], [-25, 4], [-20, 0], [-42, -3],
                           [-47, -10], [-43, -14], [-28, -10], [22, -10], [42, -13], [45, -10], [30, 0], [-43, -17],
                           [-35, -25], [27, -25], [31, -23], [40, -16]]
        self.arr_links = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [9, 10], [10, 11],
                          [11, 12], [12, 13], [13, 14], [14, 15], [15, 16], [16, 17], [17, 18], [18, 19], [19, 20],
                          [20, 21], [21, 22], [22, 23], [23, 24], [24, 25], [25, 0],
                          [20, 26], [26, 27], [27, 28], [29, 30], [30, 23]]
        self.arr_circle_centers = [[-40, -16], [37, -14], [-29, -19], [-15, -19], [-1, -19], [13, -19], [27, -19]]
        self.arr_rads = [1, 4, 6]
        self.arr_circles_cords = []

        # Начальное мастабирование изображения.
        for i in range(len(self.arr_points)):
            self.arr_points[i][0] *= self.start_scale
            self.arr_points[i][1] *= self.start_scale
        for i in range(len(self.arr_circle_centers)):
            self.arr_circle_centers[i][0] *= self.start_scale
            self.arr_circle_centers[i][1] *= self.start_scale
        for i in range(len(self.arr_rads)):
            self.arr_rads[i] *= self.start_scale

        for i in range(len(self.arr_circle_centers)):
            a = self.arr_rads[0]; b = self.arr_rads[0]; t = 0; xc = self.arr_circle_centers[i][0]; yc = self.arr_circle_centers[i][1]; h = 1 / 15
            self.arr_circles_cords.append([])
            while t <= 2 * pi:
                x = xc + a * cos(t)
                y = yc + b * sin(t)
                self.arr_circles_cords[len(self.arr_circles_cords) - 1].append([x, y])
                t += h
        for i in range(len(self.arr_circle_centers)):
            if i <= 1:
                a = self.arr_rads[1]; b = self.arr_rads[1]; t = 0; xc = self.arr_circle_centers[i][0]; yc = self.arr_circle_centers[i][1]; h = 1 / 15
                self.arr_circles_cords.append([])
                while t <= 2 * pi:
                    x = xc + a * cos(t)
                    y = yc + b * sin(t)
                    self.arr_circles_cords[len(self.arr_circles_cords) - 1].append([x, y])
                    t += h
            else:
                a = self.arr_rads[2]; b = self.arr_rads[2]; t = 0; xc = self.arr_circle_centers[i][0]; yc = self.arr_circle_centers[i][1]; h = 1 / 15
                self.arr_circles_cords.append([])
                while t <= 2 * pi:
                    x = xc + a * cos(t)
                    y = yc + b * sin(t)
                    self.arr_circles_cords[len(self.arr_circles_cords) - 1].append([x, y])
                    t += h

    # Рисование фигуры.
    def draw(self):
        scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(scene)
        h = self.graphicsView.height()
        w = self.graphicsView.width()
        scene.setSceneRect(-w/2, -h/2, w - 2, h - 2)
        if len(self.arr_points) == 0:
            self.lineEdit_center_x.setText("0")
            self.lineEdit_center_y.setText("0")
            self.graphicsView.repaint()
            return

        # Рисование кругов.
        for i in range(len(self.arr_circles_cords)):
            for j in range(len(self.arr_circles_cords[i]) - 1):
                scene.addLine(self.arr_circles_cords[i][j][0], self.arr_circles_cords[i][j][1],
                              self.arr_circles_cords[i][j + 1][0], self.arr_circles_cords[i][j + 1][1])

        # Рисование по точкам и связям.
        for i in range(len(self.arr_links)):
            scene.addLine(self.arr_points[self.arr_links[i][0]][0], self.arr_points[self.arr_links[i][0]][1],
                          self.arr_points[self.arr_links[i][1]][0], self.arr_points[self.arr_links[i][1]][1])

        self.graphicsView.repaint()

        # Обновление информации о центре фигуры.
        x = QtCore.QPointF.x(QtCore.QRectF.center(scene.itemsBoundingRect())) + 0.1
        y = QtCore.QPointF.y(QtCore.QRectF.center(scene.itemsBoundingRect()))
        self.lineEdit_center_x.setText(str(int(x)))
        self.lineEdit_center_y.setText(str(int(y)))
        self.lineEdit_XM.setText(str(int(x)))
        self.lineEdit_YM.setText(str(int(y)))
        self.lineEdit_XC.setText(str(int(x)))
        self.lineEdit_YC.setText(str(int(y)))
        self.repaint()

    # Копирование массивов для возврата на шаг назад.
    def copy(self):
        self.arr_points_buff = deepcopy(self.arr_points)
        self.arr_circle_centers_buff = deepcopy(self.arr_circle_centers)
        self.arr_rads_buff = deepcopy(self.arr_rads)
        self.arr_circles_cords_buff = deepcopy(self.arr_circles_cords)

    # Обработчик события рисования исходного изображения.
    def draw_base(self):
        self.copy()
        self.init_base_data()
        self.draw()

    # Обработчик события возврата на шаг назад.
    def step_back(self):
        self.arr_points_buff, self.arr_points = self.arr_points, self.arr_points_buff
        self.arr_circle_centers_buff, self.arr_circle_centers = self.arr_circle_centers, self.arr_circle_centers_buff
        self.arr_rads_buff, self.arr_rads = self.arr_rads, self.arr_rads_buff
        self.arr_circles_cords_buff, self.arr_circles_cords = self.arr_circles_cords, self.arr_circles_cords_buff
        self.draw()

    # Обработчик события перемещения фигуры
    def move_func(self):
        try:
            dx = int(self.lineEdit_dx.text())
            dy = int(self.lineEdit_dy.text())
        except:
            QtWidgets.QMessageBox.critical(self, "", "Расстояние переноса должно быть целым числом.")
            return
        self.copy()
        for i in range(len(self.arr_points)):
            self.arr_points[i][0] += dx; self.arr_points[i][1] += dy
        for i in range(len(self.arr_circle_centers)):
            self.arr_circle_centers[i][0] += dx; self.arr_circle_centers[i][1] += dy
        for i in range(len(self.arr_circles_cords)):
            for j in range(len(self.arr_circles_cords[i])):
                self.arr_circles_cords[i][j][0] += dx; self.arr_circles_cords[i][j][1] += dy
        self.draw()

    # Обработчик события масштабирования фигуры.
    def scale_func(self):
        try:
            kx = float(self.lineEdit_KX.text())
            ky = float(self.lineEdit_KY.text())
            xm = float(self.lineEdit_XM.text())
            ym = float(self.lineEdit_YM.text())
        except:
            QtWidgets.QMessageBox.critical(self, "", "Коэффиценты масштабирования и координаты центра масштабирования "
                                                     "должны быть целыми или вещественными числами")
            return
        self.copy()
        for i in range(len(self.arr_points)):
            self.arr_points[i][0] = self.arr_points[i][0] * kx + (1 - kx) * xm
            self.arr_points[i][1] = self.arr_points[i][1] * ky + (1 - ky) * ym
        for i in range(len(self.arr_rads)):
            self.arr_rads[i] = self.arr_rads[i] * kx
        for i in range(len(self.arr_circle_centers)):
            self.arr_circle_centers[i][0] = self.arr_circle_centers[i][0] * kx + (1 - kx) * xm
            self.arr_circle_centers[i][1] = self.arr_circle_centers[i][1] * ky + (1 - ky) * ym
        for i in range(len(self.arr_circles_cords)):
            for j in range(len(self.arr_circles_cords[i])):
                self.arr_circles_cords[i][j][0] = self.arr_circles_cords[i][j][0] * kx + (1 - kx) * xm
                self.arr_circles_cords[i][j][1] = self.arr_circles_cords[i][j][1] * ky + (1 - ky) * ym
        self.draw()

    # Обработчик события вращения фигуры.
    def rotate_func(self):
        try:
            deg = float(self.lineEdit_dg.text())
            xc = float(self.lineEdit_XC.text())
            yc = float(self.lineEdit_YC.text())
        except:
            QtWidgets.QMessageBox.critical(self, "", "Угол поворота и координаты центра поворота должны быть целыми "
                                                     "или вещественными числами.")
            return
        self.copy()
        SIN = sin(radians(deg))
        COS = cos(radians(deg))
        for i in range(len(self.arr_points)):
            x1 = xc + (self.arr_points[i][0] - xc) * COS + (self.arr_points[i][1] - yc) * SIN
            self.arr_points[i][1] = yc + (self.arr_points[i][1] - yc) * COS - (self.arr_points[i][0] - xc) * SIN
            self.arr_points[i][0] = x1
        for i in range(len(self.arr_circle_centers)):
            x1 = xc + (self.arr_circle_centers[i][0] - xc) * COS + (self.arr_circle_centers[i][1] - yc) * SIN
            self.arr_circle_centers[i][1] = yc + (self.arr_circle_centers[i][1] - yc) * COS - (self.arr_circle_centers[i][0] - xc) * SIN
            self.arr_circle_centers[i][0] = x1
        for i in range(len(self.arr_circles_cords)):
            for j in range(len(self.arr_circles_cords[i])):
                x1 = xc + (self.arr_circles_cords[i][j][0] - xc) * COS + (self.arr_circles_cords[i][j][1] - yc) * SIN
                self.arr_circles_cords[i][j][1] = yc + (self.arr_circles_cords[i][j][1] - yc) * COS - (self.arr_circles_cords[i][j][0] - xc) * SIN
                self.arr_circles_cords[i][j][0] = x1
        self.draw()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Visual()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
