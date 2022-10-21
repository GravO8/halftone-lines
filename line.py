class StraightLine:
    def __init__(self, a, b):
        '''
        The StraightLine class creates defines 2D straight lines
        A line is constructed from two points, a and b, represented by a tuple
        where position 0 and 1 represent the abscissa and ordinate, respectively
        '''
        self.slope      = (a[1]-b[1])/(a[0]-b[0]+1e-8)
        self.intercept  = a[1] - self.slope*a[0]
    def is_parallel(self, line, precision = 1e-5):
        return abs(self.slope - line.slope) < precision
    def at(self, x):
        return self.slope*x + self.intercept
    def intersection(self, line):
        if self.is_parallel(line): return False
        x = (line.intercept-self.intercept)/(self.slope-line.slope)
        y = self.at(x)
        return x,y
    def __repr__(self):
        return f"y = {round(self.slope,2)}x + {round(self.intercept,2)}"
