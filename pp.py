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
        return math.fabs(self.getMyAngle() - other.getMyAngle())%math.pi

    def get_distance(self):
        pass

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
                if obs.intersects(l):
                    cv = cv + 1

        return cv

    def getFL(self):
        d = 0
        for l in self.__lines:
            d = d + l.length
        return d

    def getFS(self):
        angles = []
        for i in range(len(self.__lines) - 1):
            angles.append(self.__lines[i].getAngle(self.__lines[i + 1]))
        return max(angles)

    def getFO(self):
        #warning this function should be changed
        min = 1000000000
        for l in self.__lines:
            for obs in obstacles:
                if l.distance(obs) < min:
                    min = l.distance(obs)
        #coefficient should be get as an input
        return  math.exp(-5 * min)

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
    class Chromosome():
        def __init__(self, genes_len, min, max):
            self.__genes_len = genes_len
            self.__genes = np.random.uniform(min, max, genes_len)

        def mutate(self, min, max):
            mutate_index = np.random.randint(0, self.__genes_len, 1)
            self.__genes_len[mutate_index] = np.random(min, max, 1)

        def crossOver(self, other):
            # cross_over_point
            cop = np.random.randint(1, self.__genes_len, 2)
            self.__genes[cop[0]: cop[1]],\
            other.getGenes()[cop[0]: cop[1]] = other.getGenes()[cop[0]: cop[1]],\
                                               self.__genes_len[cop[0]: cop[1]]
            return self

        def getGenes(self):
            return self.__genes

    #get size of population and chromosome and talent size at the first
    def __init__(self, chr_size, talent_size):
        self.__chr_size = chr_size
        self.__talentSize = talent_size
        self.__population = []

    def genPopulation(self,  max, min, pop_size):
        self.__pop_size = pop_size
        self.__population = []
        for p in range(self.__pop_size):
            self.__population.append(self.Chromosome(self.__chr_size, min, max))
        return self.__population

    def mutuation(self, chromosome, min, max):
        pass

    def crossOver(self, chromosome1, chromosome2):
        pass

    def calPopFitness(self):
        pass

    def selectMatingPool(self):
        pass

s_point_p = None
t_point_p = None
obstacles_p = []


#create robot object
grid_size = 6
r = Robot(MyPoint(0, 0), MyPoint(10, 10), grid_size + 1, None)
ga = GA(chr_size = grid_size, talent_size = 3)
g = ga.genPopulation(max=5, min=-5,pop_size=10)
print("theta robot = ", np.rad2deg(r.getTheta()))
print("g = ", g[2].getGenes())
r.updatePoints(g[2].getGenes())
p = r.getPath()
converged = True

while not converged:
    # genetic algorithm

    # 2 - cal fitness
    # 3 - select
    pass

#some function for better viewing
def addStartStopPointsToCanvas(ui, start, end):
    ui.widget.canvas.ax.plot([start.x], [start.y], 'ro', color = "blue"),
    ui.widget.canvas.ax.annotate("start", xy=(start.x, start.y), xytext = (start.x, start.y + 0.2))
    ui.widget.canvas.ax.plot([end.x], [end.y], 'ro', color = "blue")
    ui.widget.canvas.ax.annotate("end", xy=(end.x, end.y), xytext = (end.x, end.y + 0.2))

def addObstacles(ui, obstacles, color="red"):
    for obs in obstacles:
        ui.widget.canvas.ax.add_patch(obs.getDrawble(color))

def addPath(ui, p):
    ui.widget.canvas.ax.add_line(
        mlines.Line2D([p.coords[i][0] for i in range(len(p.coords))], [p.coords[i][1] for i in range(len(p.coords))],
                      color="green"))

# function that they are connected to buttons of user interface
def run(ui):
    print("run")

def result(ui):
    print("show_result")

def set_point(ui):
    r.setStartStopPoint(MyPoint(float(ui.start_x.text()), float(ui.start_y.text())),
                        MyPoint(float(ui.end_x.text()), float(ui.end_y.text())))
    #draw
    addStartStopPointsToCanvas(ui, r.getStartPoint(), r.getEndPoint())
    ui.widget.canvas.ax.autoscale(enable=True, axis='both', tight=None)
    ui.widget.canvas.draw()

def iterate(ui):
    print("iterate")
    r.updatePoints(g[2].getGenes())
    p = r.getPath()
    ui.widget.canvas.ax.clear()
    ui.widget.canvas.ax.grid(b=None, which='both', axis='both')
    addStartStopPointsToCanvas(ui, r.getStartPoint(), r.getEndPoint())
    addObstacles(ui, r.getObstacles())
    ui.widget.canvas.ax.autoscale(enable=True, axis='both', tight=None)#it can chagned the place for better feelling
    addPath(ui, p)
    ui.widget.canvas.draw()
    print("FL:{}".format(r.getFL()))
    print("FS:{}".format(r.getFS()))
    print("CV:{}".format(r.getCV()))


def reset_obstacle(ui):
    ui.widget.canvas.ax.clear()
    ui.widget.canvas.ax.grid(b=None, which='both', axis='both')
    obstacles = [Obstacle(MyPoint(random.randint(1, 20), random.randint(1, 10)), 0.5) for i in
                 range(30)]
    r.setObstacles(obstacles)
    addObstacles(ui, obstacles)
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






