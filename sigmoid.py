import numpy as np

class SigmoidPolygon:
    def __init__(self, y: int, side: int, alpha: float = 1., N: int = 10):
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
        height = height * self.alpha
        if height/self.side < 0.02:
            self.compute_points()
        else:
            y_top = (self.side-height)/2
            y_bot = height + y_top
            self.top_line.append((x*self.side+self.side/2, (y_top+self.y) ))
            self.bottom_line.append((x*self.side+self.side/2, (y_bot+self.y) ))

    def compute_points(self):
        '''
        After adding all the points using various calls to the `height` method, 
        the `compute_points` method should be called to interpolate the nice
        sigmoid polygon between the points. The points decribe the polygon's 
        outline and their order matters. The left edge is first added, then the
        upper outline is added, followed by the right edge and finally the 
        bottom outline.
        '''
        if len(self.top_line) == 0:
            return
        first_y_top     = self.top_line[0][1]
        first_y_bottom  = self.bottom_line[0][1]
        last_y_top      = self.top_line[-1][1]
        last_y_bottom   = self.bottom_line[-1][1]
        first_x         = self.top_line[0][0]-self.side/2
        points          = [(first_x,first_y_bottom), (first_x,first_y_top)] # left edge
        for i in range(len(self.top_line)-1): # upper outline
            points.extend( self.make_sigmoid(self.top_line[i],self.top_line[i+1]) )
        last_x = self.top_line[-1][0]+self.side/2
        points.extend([(last_x,last_y_top), (last_x,last_y_bottom)]) # right edge
        for i in reversed(range(len(self.bottom_line)-1)): # bottom outline
            points.extend( self.make_sigmoid(self.bottom_line[i],self.bottom_line[i+1])[::-1] )
        self.top_line    = []
        self.bottom_line = []
        self.points.append(points)
        
    def rotate(self, rotation_matrix):
        for i in range(len(self.points)):
            for j in range(len(self.points[i])):
                self.points[i][j] = tuple(rotation_matrix.dot(self.points[i][j]))
        
    def translate(self, tx = 0, ty = 0):
        for i in range(len(self.points)):
            for j in range(len(self.points[i])):
                self.points[i][j] = (self.points[i][j][0] - tx, self.points[i][j][1] - ty)

    def draw(self, draw, color: str = "black"):
        for points in self.points:
            draw.polygon(points, fill = color)
