import cv2, numpy as np
from PIL import Image, ImageDraw
from line import StraightLine
from sigmoid import SigmoidPolygon


def get_intensity(square):
    return 1-square.mean()/255

def rotation_matrix(angle: int):
    '''
    angle - angle to rotate in degrees
    Outputs an array with the correspoding (2,2) rotation matrix. See more
    details here: https://en.wikipedia.org/wiki/Rotation_matrix
    '''
    angle = np.deg2rad(angle)
    return np.array([[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]])
    
def make_edges(vertices: np.array):
    '''
    vertices -  array with shape (4,2) with the four 2D vertices that describe 
                the position of the kernel
    Outputs four a list with StraightLine objects. These lines corresponding to 
    the line segments that make up the edges of the kernel.
    '''
    edges = []
    edges.append( StraightLine(vertices[0],vertices[1]) )
    edges.append( StraightLine(vertices[2],vertices[3]) )
    edges.append( StraightLine(vertices[1],vertices[2]) )
    edges.append( StraightLine(vertices[3],vertices[0]) )
    # sanity checks
    assert edges[0].is_parallel(edges[1]), "first two edges aren't parallel"
    assert edges[2].is_parallel(edges[3]), "last two edges aren't parallel"
    return edges

def make_bbox(vertices: np.array):
    '''
    vertices -  array with shape (4,2) with the four 2D vertices that describe 
                the position of the kernel
    Outputs the minimum and maximum abscissa and ordinate integer values for all 
    the points in the vertices array. This is can be seen as the bounding box
    (bbox) that wraps the points. This method is used in the `select_kernel`
    method to avoid scanning the whole input dimensions as scanning this bbox
    is enough.
    '''
    ys = [v[1] for v in vertices]
    xs = [v[0] for v in vertices]
    return int(np.floor(min(xs))), int(np.floor(min(ys))), int(np.ceil(max(xs))), int(np.ceil(max(ys)))
    
def make_conds(edges):
    '''
    edges - a list with four StraightLine objects that describe a square. Should
            be the output of the `make_edges` method
    Returns two lambda functions that describe two 2D planes whose intersection
    define the square constructed from the edges. These conditions can be used
    to check if a point is inside the square.
    '''
    b01, b11    = edges[0].intercept, edges[1].intercept
    b21, b31    = edges[2].intercept, edges[3].intercept
    slope0      = edges[0].slope
    slope1      = edges[2].slope
    cond0       = lambda x,y: slope0*x + min(b01,b11) <= y <= slope0*x + max(b01,b11)
    cond1       = lambda x,y: slope1*x + min(b21,b31) <= y <= slope1*x + max(b21,b31)
    return cond0, cond1

def distance(pt1, pt2):
    if (pt1 is not None) and (pt2 is not None):
        return np.sqrt((pt1[0]-pt2[0])**2 + (pt1[1]-pt2[1])**2)
    return 1e10

class HalftoneLines:
    def __init__(self, img_name, kernel_s: int, bg_color: tuple, fg_color: tuple, 
    alpha: float, angle: float, N: int, side: int = None, verbose: bool = True):
        self.img        = cv2.imread(img_name, cv2.IMREAD_GRAYSCALE)
        self.img        = cv2.createCLAHE(clipLimit = 2.0, tileGridSize = (8,8)).apply(self.img)
        self.img_name   = img_name
        self.height     = self.img.shape[0]
        self.width      = self.img.shape[1]
        self.bg_color   = bg_color
        self.fg_color   = fg_color
        self.alpha      = alpha
        self.center     = np.array([self.width//2, self.height//2])
        self.r          = rotation_matrix(angle)
        self.angle      = angle
        self.kernel_s   = kernel_s
        self.N          = N
        if side is None:
            side = np.ceil(min(height,height)*0.007)
        self.side       = side
        self.zoom_ratio = self.side/self.kernel_s
        self.selection  = np.zeros((self.width,self.height), dtype = bool)
        self.canvas_r   = {} # canvas rotated
        self.diagonal1  = StraightLine((0,0),(self.width,self.height)) # descending diagonal
        self.diagonal2  = StraightLine((self.width,0),(0,self.height)) # ascending diagonal
        self.verbose    = verbose
    
    def select_kernel(self, vertices):
        '''
        vertices -  array with shape (4,2) with the four 2D vertices that 
                    describe the position of the kernel
        Outputs a tuple with two elements. The first element is a mask of the 
        current kernel position (a boolean matrix with the same dimensions of 
        the original image except for the current position of the kernel). This 
        mask is used to compute the mean grey level intensity in a sliding 
        window fashion. The second element of the tuple is the StraightLine 
        object correspoding to the bottom edge of the kernel. This edge is used 
        to determine the stop condition of the scanning process.
        '''
        edges                       = make_edges(vertices)
        cond0, cond1                = make_conds(edges)
        sel                         = np.array(self.selection, copy = True)
        min_x, min_y, max_x, max_y  = make_bbox(vertices)
        for x in range(max(0,min_x), min(max_x,self.width)):
            for y in range(max(0,min_y), min(max_y,self.height)):
                sel[x][y] = cond0(x,y) and cond1(x,y)
        return sel.T, edges[-1]
        
    def scan(self):
        self.quadrant( 1, -1)
        self.quadrant(-1, -1)
        self.quadrant(-1,  1)
        self.quadrant( 1,  1)
        
    def add_to_canvas(self, x, y, intensity):
        h = self.side * intensity
        if y in self.canvas_r:
            self.canvas_r[y]["x"].append(x)
            self.canvas_r[y]["height"].append(h)
        else:
            self.canvas_r[y] = {}
            self.canvas_r[y]["x"] = [x]
            self.canvas_r[y]["height"] = [h]
    
    def out_of_bounds(self, point: tuple):
        if point:
            return (point[0] < 0) or (point[0] > self.width) or (point[1] < 0) or (point[1] > self.height)
        return True
    
    def quadrant(self, h_sign: int, v_sign: int):
        if self.verbose:
            print(f"quadrant({h_sign},{v_sign})")
        move_h_r   = self.r.dot( np.array([self.kernel_s,0]) ) # move horizontally rotated
        move_v_r   = self.r.dot( np.array([0,self.kernel_s]) ) # move vertically rotated
        vertices   = np.array([[0, 0,                      h_sign*self.kernel_s,  h_sign*self.kernel_s], 
                               [0, v_sign*self.kernel_s,   v_sign*self.kernel_s,  0]])
        vertices_r = self.r.dot(vertices).T + self.center
        for y in range(int(1e10)):
            for x in range(int(1e10)):
                current = vertices_r + x*h_sign*move_h_r + y*v_sign*move_v_r
                sel, kernel_bottom_line = self.select_kernel(current)
                if np.any(sel):
                    self.add_to_canvas( h_sign*(0.5 + x),
                                        v_sign*(self.side/2 + y*self.side),
                                        get_intensity(self.img[sel]))
                else: # the kernel is outside the input image
                    i1 = self.diagonal1.intersection(kernel_bottom_line)
                    i2 = self.diagonal2.intersection(kernel_bottom_line)
                    d1 = distance(i1, current[0])
                    d2 = distance(i2, current[0])
                    # find the closest diagonal intersection with the current row
                    if d1 < d2:
                        # if the intersection is out of bonds OR
                        # is within bounds but can't be reached
                        # stop the current x iteration loop
                        if self.out_of_bounds(i1) or (np.sign(i1[0]-current[0][0]) != h_sign):
                            break
                    else:
                        if self.out_of_bounds(i2) or (np.sign(i2[0]-current[0][0]) != h_sign):
                            break
            if x == 0: 
                # python allows to access loop variables outside their block scope
                # when x is 0, the kernel is in a row where neither the first kernel
                # position nor any position left/right to it intesects the image
                # every other row above/bellow this row will be in the same situation
                # so we can exit the outer y iteration loop
                # I write "left/right" and "above/bellow" because these directions
                # depend on the quadrant being scanned
                break
    
    def draw_canvas(self):
        img_out         = Image.new("RGB", 
                                    (int(self.width*self.zoom_ratio), 
                                    int(self.height*self.zoom_ratio)), 
                                    self.bg_color)
        draw            = ImageDraw.Draw(img_out)
        self.canvas_r   = dict(sorted(self.canvas_r.items())) # sorts the dictionary by key, i.e. by y
        tx, ty, c       = 1e10, 1e10, 0
        lines           = []
        for y in self.canvas_r:
            line    = SigmoidPolygon(c*self.side, self.side, alpha = self.alpha, N = self.N)
            x       = np.array(self.canvas_r[y]["x"])
            # sort the abscissas and their respective heights
            i_sort  = np.argsort(x)
            x       = x[i_sort]
            height  = np.array(self.canvas_r[y]["height"])[i_sort]
            for i in range(len(x)):
                line.height(x[i], height[i])
            line.compute_points()
            x_min, y_min = line.rotate(self.r)
            tx           = min(x_min, tx)
            ty           = min(y_min, ty)
            c           += 1
            lines.append(line)
        tx += self.side*np.sin(np.deg2rad(self.angle))
        ty += self.side*np.sin(np.deg2rad(self.angle))
        for line in lines:
            line.translate(tx, ty)
            line.draw(draw, color = self.fg_color)
        img_out.save("out-" + self.img_name)
        if self.verbose:
            print("done")
        
    def halftone(self):
        self.scan()
        self.draw_canvas()
