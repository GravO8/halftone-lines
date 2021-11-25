class SigmoidPolygon:
    def __init__(self, y: int, max_height: int, slope: float = 1., N: int = 10):
        N                   = N//2
        self.ts             = [t/N for t in range(-N, N)]
        self.y              = y
        self.max_height     = max_height
        self.slope          = slope
        self.top_line       = []
        self.bottom_line    = []
        self.points         = []

    def make_sigmoid(self, pair):
        pass

    def height(self, x, height):
        y_top  = (self.max_height-height)/2
        y_bot  = height + y_top
        self.top_line.append((x,y_top))
        self.bottom_line.append((x,y_bot))

    def compute_points(self):
        first_y_top     = self.top_line[0][1]
        first_y_bottom  = self.bottom_line[0][1]
        last_y_top      = self.top_line[-1][1]
        last_y_bottom   = self.bottom_line[-1][1]
        self.points     = [(0,first_y_bottom), (0,first_y_top)]
        for i in range(len(self.top_line)-1):
            self.points.extend( self.make_sigmoid(self.top_line[i],self.top_line[i+1]) )
        last_x = len(self.top_line)*max_height - 1
        self.points.extend([(last_x,last_y_top), (last_x,last_y_bottom)])
        for i in reversed(range(len(self.bottom_line)-1)):
            self.points.extend( self.make_sigmoid(self.bottom_line[i],self.bottom_line[i+1])[::-1] )

    def draw(self, draw, color: str = "black"):
        if len(self.points) == 0:
            self.compute_points()
        draw.polygon(self.points, fill = color)


if __main__ == "__main__":
    import matplotlib.pyplot as plt
    import numpy as np

    Y_TOP = 0
    Y_BOT = 1
    SLOPE = 5

    def sigmoid(x):
        return (Y_TOP-Y_BOT)*(1/(1 + np.exp(-x*SLOPE))) + Y_BOT

    x = [i/100 for i in range(-1000,1000)]
    y = [sigmoid(e) for e in x]

    plt.figure(figsize = (20,6))
    plt.plot(x,y)
    plt.axis("equal")
    plt.grid(True)
    plt.show()
