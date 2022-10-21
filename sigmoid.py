import numpy as np

class SigmoidPolygon:
    def __init__(self, y: int, side: int, alpha: float = 1., N: int = 2):
        '''
        The SigmoidPolygon class defines the lines that are drawn in the output
        image. These lines have a dynamic width proportional to the grey level 
        intensity of the corresponding square in the original image. Each square
        in the original image is mapped to a square of side `side` in the output
        image. The width of the line smoothly changes using a sigmoid function.
        y     - y position of the polygon in the output image
        side  - the height of the polygon (and the side size of each square that
                makes up the polygon)
        alpha - controls how width of the sigmoid. The higher alphas the wide 
                the line will be
        N     - number of points to interpolate the sigmoid line
        '''
        self.N              = N
        self.y              = y
        self.side           = side
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
        '''
        Function that actually populates the polygon
        x      - position of the new point
        height - height of the new point, how wide it should be
        '''
        assert height <= self.side
        y_top  = (self.side-height)/2
        y_bot  = height + y_top
        self.top_line.append((x*self.side+self.side/2,y_top+self.y-self.alpha))
        self.bottom_line.append((x*self.side+self.side/2,y_bot+self.y+self.alpha))

    def compute_points(self):
        '''
        After adding all the points using various calls to the `height` method, 
        the `compute_points` method should be called to interpolate the nice
        sigmoid polygon between the points 
        '''
        first_y_top     = self.top_line[0][1]
        first_y_bottom  = self.bottom_line[0][1]
        last_y_top      = self.top_line[-1][1]
        last_y_bottom   = self.bottom_line[-1][1]
        # first_x         = (self.top_line[0][0]-0.5)*self.side
        first_x         = self.top_line[0][0]-self.side/2
        self.points     = [(first_x,first_y_bottom), (first_x,first_y_top)]
        for i in range(len(self.top_line)-1):
            self.points.extend( self.make_sigmoid(self.top_line[i],self.top_line[i+1]) )
        # last_x = len(self.top_line)*self.side - 1
        last_x = self.top_line[-1][0]+self.side/2
        self.points.extend([(last_x,last_y_top), (last_x,last_y_bottom)])
        for i in reversed(range(len(self.bottom_line)-1)):
            self.points.extend( self.make_sigmoid(self.bottom_line[i],self.bottom_line[i+1])[::-1] )

    def draw(self, draw, color: str = "black"):
        if len(self.points) == 0:
            self.compute_points()
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
