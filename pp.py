from PyQt5.QtWidgets import QApplication, QMainWindow
from ui.pp_ui import Ui_MainWindow
from PyQt5 import QtWidgets
import sys
import math
from shapely.geometry import Polygon
from descartes import PolygonPatch

class Obstacle(Polygon):
    class Point:
        def __init__(self, x, y):
            self.x = x
            self.y = y
        def __add__(self, other):
            return (self.x + other.x, self.y + other.y)

    def __init__(self, center_point, size):
        super().__init__()
        self.center = center_point
        corners = [ self.Point(-1, -1), self.Point(-1, 1), self.Point(1, 1), self.Point(1, -1) ]
        new_corners = [ c+center_point for c in corners]
        self.p = Polygon(new_corners)

    def getDrawble(self, color):
        return PolygonPatch(self.p, color=color)
#Ui class
class Ui(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

# Create GUI application
app = QtWidgets.QApplication(sys.argv)
form = Ui()
for i in range(10):
    form.widget.canvas.ax.add_patch(Obstacle(Obstacle.Point(i,i), 1).getDrawble("red"))
form.widget.canvas.ax.autoscale(enable=True, axis='both', tight=None)
form.widget.canvas.ax.grid(b=None, which='both', axis='both')
form.show()
app.exec_()





