# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1167, 682)
        MainWindow.setMinimumSize(QtCore.QSize(1167, 682))
        MainWindow.setMaximumSize(QtCore.QSize(1167, 682))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setMinimumSize(QtCore.QSize(780, 660))
        self.graphicsView.setMaximumSize(QtCore.QSize(780, 660))
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 0, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.Parameters = QtWidgets.QGroupBox(self.centralwidget)
        self.Parameters.setMinimumSize(QtCore.QSize(341, 151))
        self.Parameters.setMaximumSize(QtCore.QSize(341, 151))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Parameters.setFont(font)
        self.Parameters.setObjectName("Parameters")
        self.labelColor = QtWidgets.QLabel(self.Parameters)
        self.labelColor.setGeometry(QtCore.QRect(-20, 30, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelColor.setFont(font)
        self.labelColor.setStyleSheet("")
        self.labelColor.setAlignment(QtCore.Qt.AlignCenter)
        self.labelColor.setObjectName("labelColor")
        self.colorBox = QtWidgets.QComboBox(self.Parameters)
        self.colorBox.setGeometry(QtCore.QRect(170, 30, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.colorBox.setFont(font)
        self.colorBox.setStyleSheet("")
        self.colorBox.setObjectName("colorBox")
        self.colorBox.addItem("")
        self.colorBox.addItem("")
        self.colorBox.addItem("")
        self.colorBox.addItem("")
        self.labelMethod = QtWidgets.QLabel(self.Parameters)
        self.labelMethod.setGeometry(QtCore.QRect(0, 70, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelMethod.setFont(font)
        self.labelMethod.setStyleSheet("")
        self.labelMethod.setAlignment(QtCore.Qt.AlignCenter)
        self.labelMethod.setObjectName("labelMethod")
        self.paintBox = QtWidgets.QComboBox(self.Parameters)
        self.paintBox.setGeometry(QtCore.QRect(170, 70, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.paintBox.setFont(font)
        self.paintBox.setStyleSheet("")
        self.paintBox.setObjectName("paintBox")
        self.paintBox.addItem("")
        self.paintBox.addItem("")
        self.delay = QtWidgets.QLineEdit(self.Parameters)
        self.delay.setGeometry(QtCore.QRect(170, 110, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.delay.setFont(font)
        self.delay.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.delay.setObjectName("delay")
        self.labelDelay = QtWidgets.QLabel(self.Parameters)
        self.labelDelay.setGeometry(QtCore.QRect(0, 110, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelDelay.setFont(font)
        self.labelDelay.setStyleSheet("")
        self.labelDelay.setAlignment(QtCore.Qt.AlignCenter)
        self.labelDelay.setObjectName("labelDelay")
        self.verticalLayout.addWidget(self.Parameters)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setMinimumSize(QtCore.QSize(341, 121))
        self.groupBox_2.setMaximumSize(QtCore.QSize(341, 121))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontal = QtWidgets.QRadioButton(self.groupBox_2)
        self.horizontal.setGeometry(QtCore.QRect(10, 60, 311, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.horizontal.setFont(font)
        self.horizontal.setObjectName("horizontal")
        self.nomode = QtWidgets.QRadioButton(self.groupBox_2)
        self.nomode.setGeometry(QtCore.QRect(10, 30, 311, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.nomode.setFont(font)
        self.nomode.setChecked(True)
        self.nomode.setObjectName("nomode")
        self.vertical = QtWidgets.QRadioButton(self.groupBox_2)
        self.vertical.setGeometry(QtCore.QRect(10, 90, 311, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.vertical.setFont(font)
        self.vertical.setChecked(False)
        self.vertical.setObjectName("vertical")
        self.verticalLayout.addWidget(self.groupBox_2)
        self.inputMode = QtWidgets.QPushButton(self.centralwidget)
        self.inputMode.setMinimumSize(QtCore.QSize(321, 41))
        self.inputMode.setMaximumSize(QtCore.QSize(321, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.inputMode.setFont(font)
        self.inputMode.setObjectName("inputMode")
        self.verticalLayout.addWidget(self.inputMode)
        self.paintBut = QtWidgets.QPushButton(self.centralwidget)
        self.paintBut.setMinimumSize(QtCore.QSize(321, 41))
        self.paintBut.setMaximumSize(QtCore.QSize(321, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.paintBut.setFont(font)
        self.paintBut.setStyleSheet("")
        self.paintBut.setObjectName("paintBut")
        self.verticalLayout.addWidget(self.paintBut)
        self.cancel = QtWidgets.QPushButton(self.centralwidget)
        self.cancel.setMinimumSize(QtCore.QSize(321, 41))
        self.cancel.setMaximumSize(QtCore.QSize(321, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.cancel.setFont(font)
        self.cancel.setObjectName("cancel")
        self.verticalLayout.addWidget(self.cancel)
        self.clean = QtWidgets.QPushButton(self.centralwidget)
        self.clean.setMinimumSize(QtCore.QSize(321, 41))
        self.clean.setMaximumSize(QtCore.QSize(321, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.clean.setFont(font)
        self.clean.setObjectName("clean")
        self.verticalLayout.addWidget(self.clean)
        spacerItem = QtWidgets.QSpacerItem(20, 208, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.paintBox.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Parameters.setTitle(_translate("MainWindow", "Параметры закраски"))
        self.labelColor.setText(_translate("MainWindow", "Цвет:"))
        self.colorBox.setItemText(0, _translate("MainWindow", "Черный"))
        self.colorBox.setItemText(1, _translate("MainWindow", "Красный"))
        self.colorBox.setItemText(2, _translate("MainWindow", "Зеленый"))
        self.colorBox.setItemText(3, _translate("MainWindow", "Синий"))
        self.labelMethod.setText(_translate("MainWindow", "Способ закраски:"))
        self.paintBox.setItemText(0, _translate("MainWindow", "С задержкой"))
        self.paintBox.setItemText(1, _translate("MainWindow", "Без задержки"))
        self.delay.setText(_translate("MainWindow", "1"))
        self.labelDelay.setText(_translate("MainWindow", "Задержка:"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Выбор режима отрисовки линий"))
        self.horizontal.setText(_translate("MainWindow", "Рисовать горизонтальные линии"))
        self.nomode.setText(_translate("MainWindow", "Рисовать произвольные линии"))
        self.vertical.setText(_translate("MainWindow", "Рисовать вертикальные линии"))
        self.inputMode.setText(_translate("MainWindow", "Вкл/Выкл ввод фигуры"))
        self.paintBut.setText(_translate("MainWindow", "Закрасить"))
        self.cancel.setText(_translate("MainWindow", "Отменить закраску"))
        self.clean.setText(_translate("MainWindow", "Очистить"))