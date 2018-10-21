# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pp.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1041, 702)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.reset_points = QtWidgets.QPushButton(self.centralwidget)
        self.reset_points.setGeometry(QtCore.QRect(10, 610, 161, 27))
        self.reset_points.setObjectName("reset_points")
        self.reset_obstacles = QtWidgets.QPushButton(self.centralwidget)
        self.reset_obstacles.setGeometry(QtCore.QRect(190, 610, 161, 27))
        self.reset_obstacles.setObjectName("reset_obstacles")
        self.start = QtWidgets.QPushButton(self.centralwidget)
        self.start.setGeometry(QtCore.QRect(670, 610, 97, 27))
        self.start.setObjectName("start")
        self.iterate = QtWidgets.QPushButton(self.centralwidget)
        self.iterate.setGeometry(QtCore.QRect(800, 610, 97, 27))
        self.iterate.setObjectName("iterate")
        self.run = QtWidgets.QPushButton(self.centralwidget)
        self.run.setGeometry(QtCore.QRect(930, 610, 97, 27))
        self.run.setObjectName("run")
        self.set_points = QtWidgets.QPushButton(self.centralwidget)
        self.set_points.setGeometry(QtCore.QRect(10, 640, 97, 27))
        self.set_points.setObjectName("set_points")
        self.widget = MplWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(-2, 10, 1041, 591))
        self.widget.setObjectName("widget")
        self.start_x = QtWidgets.QLineEdit(self.centralwidget)
        self.start_x.setGeometry(QtCore.QRect(220, 640, 113, 27))
        self.start_x.setText("")
        self.start_x.setObjectName("start_x")
        self.start_y = QtWidgets.QLineEdit(self.centralwidget)
        self.start_y.setGeometry(QtCore.QRect(440, 640, 113, 27))
        self.start_y.setObjectName("start_y")
        self.end_x = QtWidgets.QLineEdit(self.centralwidget)
        self.end_x.setGeometry(QtCore.QRect(660, 640, 113, 27))
        self.end_x.setObjectName("end_x")
        self.end_y = QtWidgets.QLineEdit(self.centralwidget)
        self.end_y.setGeometry(QtCore.QRect(910, 640, 113, 27))
        self.end_y.setObjectName("end_y")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(160, 640, 51, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(380, 640, 51, 20))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(610, 640, 41, 20))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(860, 640, 41, 20))
        self.label_4.setObjectName("label_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1041, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "pathplanning"))
        self.reset_points.setText(_translate("MainWindow", "reset start stop points"))
        self.reset_obstacles.setText(_translate("MainWindow", "reset obstacles"))
        self.start.setText(_translate("MainWindow", "start"))
        self.iterate.setText(_translate("MainWindow", "iterate"))
        self.run.setText(_translate("MainWindow", "run"))
        self.set_points.setText(_translate("MainWindow", "set points"))
        self.label.setText(_translate("MainWindow", "start x"))
        self.label_2.setText(_translate("MainWindow", "start y"))
        self.label_3.setText(_translate("MainWindow", "end x"))
        self.label_4.setText(_translate("MainWindow", "end y"))

from mplwidget import MplWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

