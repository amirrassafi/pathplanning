from PyQt5.QtWidgets import QApplication, QMainWindow
from ui.pp_ui import Ui_MainWindow
from PyQt5 import QtWidgets
import sys

import math

from shapely.geometry import Polygon
from shapely.geometry import Point
from shapely.geometry import LineString

from descartes import PolygonPatch
import random

class myPoint(Point):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __add__(self, other):
        return myPoint(self.x + other.x, self.y + other.y)

    def scale(self, ratio):
        return myPoint(self.x * ratio, self.y * ratio)

    def getXy(self):
        return (self.x, self.y)

class Obstacle(Polygon):

    def __init__(self, center_point, size = 1):
        super().__init__()
        self.center = center_point
        corners = [myPoint(-1, -1), myPoint(-1, 1), myPoint(1, 1), myPoint(1, -1) ]
        corners = [p.scale(size) for p in corners]
        new_corners = [c+center_point for c in corners]
        self.p = Polygon([(p.x, p.y) for p in new_corners])

    def getDrawble(self, color):
        return PolygonPatch(self.p, color=color)

class GA:
    #get size of population and chromosome and talent size at the first
    def __init__(self, popSize, chSize, talentSize):
        self.__chromosome_size = chSize
        self.__population_size = popSize
        self.__population = []

    def genPopulation(self, size, max, min):
        self.__population = []
        for p in range(self.__population_size):
            chromosome = []
            for i in range(size):
                chromosome.append(random.randint(min, max))
            self.__population.append(chromosome)
        return self.__population

    def mutuation(self):
        pass

    def crossOver(self):
        pass


class Robot:
    def __init__(self, start_point, end_point, grid_num, obstacles):
        self.__s_point = start_point
        self.__t_point = end_point
        self.__point_num = grid_num
        self.__obstacles = obstacles
        self.__st_line = LineString([self.__s_point.getXy(), self.__t_point.getXy()])
        self.__theta = math.degrees(math.atan2(end_point.y - start_point.x,end_point.x - start_point.x))
        print(self.__theta)
        self.__points = []
        self.__ga = GA(popSize=10, chSize=self.__point_num, talentSize=5)
        #this line should be edited beacuse of wrong min and max...min and max should depend on path!
        self.__candidate_point = self.__ga.genPopulation(10, 1, 1)

    def getCV(self):
        pass

    def getFL(self):
        pass

    def getFS(self):
        pass

    def getFO(self, obstacles):
        pass
    # return a line from start to stop
    def getSTLine(self):
        return self.__st_line

    def getStartPoint(self):
        return self.__s_point

    def getEndPoint(self):
        return self.__t_point




#Ui class
class Ui(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)


obstacles = [Obstacle(myPoint(random.randint(1, 20), random.randint(1, 10)), 0.5).getDrawble("red") for i in range(20)]
r = Robot(myPoint(random.randint(1, 20), random.randint(1, 20)), myPoint(random.randint(1, 20), random.randint(1, 20)), 5, obstacles)
# Create GUI application
app = QtWidgets.QApplication(sys.argv)
form = Ui()
for obs in obstacles:
    form.widget.canvas.ax.add_patch(obs)
form.widget.canvas.ax.plot([r.getStartPoint().x], [r.getStartPoint().y], 'ro', color = "blue")
form.widget.canvas.ax.annotate("start", xy=(r.getStartPoint().x, r.getStartPoint().y), xytext = (r.getStartPoint().x, r.getStartPoint().y + 0.2))
form.widget.canvas.ax.plot([r.getEndPoint().x], [r.getEndPoint().y], 'ro', color = "blue")
form.widget.canvas.ax.annotate("end", xy=(r.getEndPoint().x, r.getEndPoint().y), xytext = (r.getEndPoint().x, r.getEndPoint().y + 0.2))

print(r.getStartPoint().getXy())
form.widget.canvas.ax.autoscale(enable=True, axis='both', tight=None)
form.widget.canvas.ax.grid(b=None, which='both', axis='both')
form.show()
app.exec_()





