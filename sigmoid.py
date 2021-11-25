import matplotlib.pyplot as plt
import numpy as np

Y_TOP = 1
Y_BOT = 0
SLOPE = 5

class SigmoidPolygon:
    def __init__(self, y: int, slope: float = 1., N: int = 10):
        self.ts         = [t/N for t in range(N+1)]
        self.y          = y
        self.slope      = slope
        
    def make_sigmoid(self):

    def extend(self, xys: list):
        xys     = [(e[0],e[1]+self.y) for e in xys]
        sig     = self.make_sigmoid(xys)
        self.points.extend(bezier(self.ts))
        
    def extend_top(self, point: tuple):
        self.top.append((point[0],point[1]+self.y))
    def extend_bottom(self, point: tuple):
        self.bottom.append((point[0],point[1]+self.y))
        
    def draw(self, draw, color: str = "black"):
        draw.polygon(self.points, fill = color)


def sigmoid(x):
    return (Y_TOP-Y_BOT)*(1/(1 + np.exp(-x*SLOPE))) + Y_BOT

x = [i/100 for i in range(-1000,1000)]
y = [sigmoid(e) for e in x]

plt.figure(figsize = (20,6))
plt.plot(x,y)
plt.axis("equal")
plt.grid(True)
plt.show()
