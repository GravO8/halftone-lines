import numpy as np

class SigmoidPolygon:
    def __init__(self, y: int, max_height: int, alpha: float = 1., N: int = 10):
        self.N              = N
        self.y              = y
        self.max_height     = max_height
        self.alpha          = alpha
        self.top_line       = []
        self.bottom_line    = []
        self.points         = []

    def make_sigmoid(self, start, end):
        x_start, y_start    = start
        x_end, y_end        = end
        xs                  = np.arange(x_start, x_end, (x_end-x_start)*self.N)
        sigmoid             = lambda x: (y_start + (y_end-y_start)/(1+np.exp(-x)))
        return [(x,sigmoid(x)) for x in xs]

    def height(self, x, height):
        y_top  = (self.max_height-height)/2
        y_bot  = height + y_top
        self.top_line.append((x*self.max_height+self.max_height/2,y_top+self.y-self.alpha))
        self.bottom_line.append((x*self.max_height+self.max_height/2,y_bot+self.y+self.alpha))

    def compute_points(self):
        first_y_top     = self.top_line[0][1]
        first_y_bottom  = self.bottom_line[0][1]
        last_y_top      = self.top_line[-1][1]
        last_y_bottom   = self.bottom_line[-1][1]
        self.points     = [(0,first_y_bottom), (0,first_y_top)]
        for i in range(len(self.top_line)-1):
            self.points.extend( self.make_sigmoid(self.top_line[i],self.top_line[i+1]) )
        last_x = len(self.top_line)*self.max_height - 1
        self.points.extend([(last_x,last_y_top), (last_x,last_y_bottom)])
        for i in reversed(range(len(self.bottom_line)-1)):
            self.points.extend( self.make_sigmoid(self.bottom_line[i],self.bottom_line[i+1])[::-1] )

    def draw(self, draw, color: str = "black"):
        if len(self.points) == 0:
            self.compute_points()
        # print(self.points)
        draw.polygon(self.points, fill = color)


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    y_end   = 1
    y_start = 0
    x_start = -1000
    x_end   = 1000
    SLOPE   = 10000

    def sigmoid(x):
        return (y_start + (y_end-y_start)/(1+np.exp(-x*SLOPE)))

    # x = np.arange(x_start, x_end, (x_end-x_start)/100)
    x = [i/100 for i in range(-1000,1000)]
    y = [sigmoid(e) for e in x]

    plt.figure(figsize = (20,6))
    plt.plot(x,y)
    plt.axis("equal")
    plt.grid(True)
    plt.show()
