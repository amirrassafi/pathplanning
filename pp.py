from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
sys.path.insert(0, "./ui/")
from ui.pp_ui import Ui_MainWindow
from PyQt5 import QtWidgets
import math
import numpy as np
from shapely.geometry import Polygon
from shapely.geometry import Point
from shapely.geometry import LineString
from descartes import PolygonPatch
import random
import matplotlib.lines as mlines


class MyPoint(Point):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __add__(self, other):
        return MyPoint(self.x + other.x, self.y + other.y)

    def scale(self, ratio):
        return MyPoint(self.x * ratio, self.y * ratio)

    def getXy(self):
        return (self.x, self.y)

    def rotate(self, theta):
        c, s = np.cos(theta), np.sin(theta)
        r = np.array([[c, -s], [s, c]])
        new_xy = list(np.matmul(r, self.getXy()))
        return MyPoint(new_xy[0], new_xy[1])

class MyLineString(LineString):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def getMyAngle(self):
        return math.atan2(self.coords[1][1] - self.coords[0][1],
                          self.coords[1][0] - self.coords[0][0])

    def getAngle(self, other):
        return math.fabs(self.getMyAngle() - other.getMyAngle())%180

class Obstacle(Polygon):

    def __init__(self, center_point, size = 1):
        self.center = center_point
        corners = [MyPoint(-1, -1), MyPoint(-1, 1), MyPoint(1, 1), MyPoint(1, -1)]
        corners = [p.scale(size) for p in corners]
        new_corners = [c+center_point for c in corners]
        self.p = Polygon([(p.x, p.y) for p in new_corners])
        super().__init__(self.p)

    def getDrawble(self, color):
        return PolygonPatch(self.p, color=color)

    def getCenter(self):
        return self.center

class Robot:
    def __init__(self, start_point, end_point, grid_num, obstacles):
        self.__s_point = start_point
        self.__t_point = end_point
        self.__point_num = grid_num
        self.__obstacles = obstacles
        self.__createStLine()

    def __createStLine(self):
        self.__st_line = MyLineString([self.__s_point.getXy(), self.__t_point.getXy()])
        self.__theta = math.atan2(self.__t_point.y - self.__s_point.y,
                                  self.__t_point.x - self.__s_point.x)
        self.__x_prime_array = np.arange(0, self.__st_line.length+self.__st_line.length/self.__point_num,
                                         self.__st_line.length/self.__point_num)
        self.__points = [MyPoint(x, 0) for x in self.__x_prime_array]
        self.__lines = []

    def setStartStopPoint(self, s_point, t_point):
        self.__s_point = s_point
        self.__t_point = t_point
        self.__createStLine()

    def setObstacles(self, obstacles):
        self.__obstacles = obstacles

    def updatePoints(self, points):
        #here should have bug fixed
        points = [0]+points+[0]
        self.__points = [MyPoint(x, y).rotate(self.__theta) for x, y in zip(self.__x_prime_array, points)]
        #print("points", [p.getXy() for p in self.__points])
        self.__points = [MyPoint(p.x, p.y) + self.__s_point for p in self.__points]
        print("points", [p.getXy() for p in self.__points])
        self.__lines = [MyLineString([p1.getXy(), p2.getXy()]) for
                        p1, p2 in zip([self.__s_point] + self.__points,
                                      self.__points+[self.__t_point])]

    def getCV(self):
        cv = 0
        for l in self.__lines:
            for obs in self.__obstacles:
                if l.intersects(obs):
                    cv = cv + 1
        return cv

    def getFL(self):
        d = 0
        for l in self.__lines:
            d = d + l.length

    def getFS(self):
        angles = []
        for i in range(len(self.__lines) - 1):
            angles.append(self.__lines[i].getAngle(i + 1))
        return max(angles)

    def getFO(self):
        #warning this function should be changed
        min = 1000000000
        for l in self.__lines:
            for obs in obstacles:
                if l.distance(obs) < min:
                    min = l.distance(obs)
        return min

    # return a line from start to stop
    def getSTLine(self):
        return self.__st_line

    def getStartPoint(self):
        return self.__s_point

    def getEndPoint(self):
        return self.__t_point

    def getPath(self):
        return LineString([p.getXy() for p in self.__points])

    def getTheta(self):
        return self.__theta

    def getObstacles(self):
        return self.__obstacles

class GA:
    #get size of population and chromosome and talent size at the first
    def __init__(self, popSize, chSize, talentSize):
        self.__chromosome_size = chSize
        self.__population_size = popSize
        self.__talentSize = talentSize
        self.__population = []
        self.__chromosome = []

    def genPopulation(self,  max, min):
        self.__population = []
        self.__chromosome = []
        for p in range(self.__population_size):
            self.__population.append(list(np.random.uniform(low = min, high = max, size = self.__chromosome_size)))
        return self.__population

    def mutuation(self, chromosome, min, max):
        place = np.random.randint(0, len(chromosome), 1)
        chromosome[int(place)] = np.random.uniform(min, max, 1)

    def crossOver(self, chromosome1, chromosome2):
        #cross_over_point
        cop = np.random.randint(1, self.__chromosome_size, 2)
        chromosome1[cop[0]: cop[1]], chromosome2[cop[0]: cop[1]] = chromosome2[cop[0]: cop[1]], chromosome1[cop[0]: cop[1]]

    def calPopFitness(self):
        pass

    def selectMatingPool(self):
        pass

s_point_p = None
t_point_p = None
obstacles_p = []

#create robot object
r = Robot(MyPoint(0, 0), MyPoint(10, 10), 10, None)
ga = GA(5, 9, 3)
g = ga.genPopulation(-5, 5)
print("theta robot = ", np.rad2deg(r.getTheta()))
print("g = ", g[2])
r.updatePoints(g[2])
p = r.getPath()
#robot = Robot(MyPoint(int(self.start_x.text()), int(self.start_y.text())), MyPoint(int(self.end_x.text()), int(self.end_y.text())), 10, obstacles)


#genetic algorithm
#1 - generate first population
#2 - cal fitness
#3 - select


def run(ui):
    print("run")

def result(ui):
    print("show_result")

def set_point(ui):
    r.setStartStopPoint(MyPoint(float(ui.start_x.text()), float(ui.start_y.text())),
                        MyPoint(float(ui.end_x.text()), float(ui.end_y.text())))
    #draw
    ui.widget.canvas.ax.plot([r.getStartPoint().x], [r.getStartPoint().y], 'ro', color = "blue"),
    ui.widget.canvas.ax.annotate("start", xy=(r.getStartPoint().x, r.getStartPoint().y), xytext = (r.getStartPoint().x, r.getStartPoint().y + 0.2))
    ui.widget.canvas.ax.plot([r.getEndPoint().x], [r.getEndPoint().y], 'ro', color = "blue")
    ui.widget.canvas.ax.annotate("end", xy=(r.getEndPoint().x, r.getEndPoint().y), xytext = (r.getEndPoint().x, r.getEndPoint().y + 0.2))
    ui.widget.canvas.ax.autoscale(enable=True, axis='both', tight=None)
    ui.widget.canvas.draw()

def iterate(ui):
    print("iterate")
    r.updatePoints(g[2])
    p = r.getPath()
    for q in p.coords:
        print(q)
    ui.widget.canvas.ax.add_line(
        mlines.Line2D([p.coords[i][0] for i in range(len(p.coords))], [p.coords[i][1] for i in range(len(p.coords))],
                      color="green"))
    ui.widget.canvas.ax.autoscale(enable=True, axis='both', tight=None)
    ui.widget.canvas.draw()

def reset_obstacle(ui):
    ui.widget.canvas.ax.clear()
    ui.widget.canvas.ax.grid(b=None, which='both', axis='both')
    obstacles = [Obstacle(MyPoint(random.randint(1, 20), random.randint(1, 10)), 0.5).getDrawble("red") for i in
                 range(30)]
    r.setObstacles(obstacles)
    for obs in obstacles:
        ui.widget.canvas.ax.add_patch(obs)
    ui.widget.canvas.ax.autoscale(enable=True, axis='both', tight=None)
    ui.widget.canvas.draw()
    print("show obs")

#Ui class
class Ui(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.run.clicked.connect(lambda: run(self))
        self.reset_obstacles.clicked.connect(lambda: reset_obstacle(self))
        self.set_points.clicked.connect(lambda: set_point(self))
        self.iterate.clicked.connect(lambda: iterate(self))
        self.result.clicked.connect(lambda: result(self))
        self.widget.canvas.ax.grid(b=None, which='both', axis='both')

# Create GUI application

app = QtWidgets.QApplication(sys.argv)
form = Ui()
form.show()
app.exec_()





