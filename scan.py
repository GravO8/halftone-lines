import cv2
import numpy as np
from PIL import Image, ImageDraw
from sigmoid import SigmoidPolygon

def get_intensity(square):
    return 1-square.mean()/255

def rotation_matrix(angle):
    angle = np.deg2rad(angle)
    return np.array([[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]])
    
def make_edges(vertices):
    '''
    Outputs the four edges of the tilted square. Two parallel sides at the time.
    '''
    edges = []
    edges.append( StraightLine(vertices[0],vertices[1]) )
    edges.append( StraightLine(vertices[2],vertices[3]) )
    edges.append( StraightLine(vertices[1],vertices[2]) )
    edges.append( StraightLine(vertices[-1],vertices[0]) )
    assert edges[0].is_parallel(edges[1]), "first two edges aren't parallel"
    assert edges[2].is_parallel(edges[3]), "last two edges aren't parallel"
    return edges

def make_bbox(vertices):
    '''
    No need to scan the entire image to make the selection, just the bounding 
    box (bbox) that wrapps the tilted square
    '''
    ys = [v[1] for v in vertices]
    xs = [v[0] for v in vertices]
    return int(np.floor(min(xs))), int(np.floor(min(ys))), int(np.ceil(max(xs))), int(np.ceil(max(ys)))
    
def make_conds(edges):
    '''
    Creates the conditions that checks if a point is whithin the tilted square
    '''
    b01, b11    = edges[0].intercept, edges[1].intercept
    b21, b31    = edges[2].intercept, edges[3].intercept
    slope0      = edges[0].slope
    slope1      = edges[2].slope
    cond0       = lambda x,y: slope0*x + min(b01,b11) <= y <= slope0*x + max(b01,b11)
    cond1       = lambda x,y: slope1*x + min(b21,b31) <= y <= slope1*x + max(b21,b31)
    return cond0, cond1
    
class StraightLine:
    def __init__(self, a, b):
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

class Scan:
    def __init__(self, img, kernel_s, side, angle):
        self.img        = img
        self.height     = self.img.shape[0]
        self.width      = self.img.shape[1]
        self.x_center   = self.width//2
        self.y_center   = self.height//2
        self.r          = rotation_matrix(angle)
        self.kernel_s   = kernel_s
        self.angle      = angle
        self.side       = side
        self.selection  = np.zeros((self.width,self.height), dtype = bool)
        self.canvas_r   = {} # canvas rotated
        self.color      = 255
        self.c          = 0
        self.diagonal1  = StraightLine((0,0),(self.width,self.height))
        self.diagonal2  = StraightLine((self.width,0),(0,self.height))
    
    def select_square(self, vertices):
        edges                       = make_edges(vertices)
        cond0, cond1                = make_conds(edges)
        sel                         = np.array(self.selection, copy = True)
        min_x, min_y, max_x, max_y  = make_bbox(vertices)
        for x in range(max(0,min_x), min(max_x,self.width)):
            for y in range(max(0,min_y), min(max_y,self.height)):
                sel[x][y] = cond0(x,y) and cond1(x,y)
        return sel.T, edges[-1]
        
    def scan(self):
        self.quadrant(1, -1)
        self.quadrant(-1, -1)
        self.quadrant(-1, 1)
        self.quadrant(1, 1)
        cv2.imwrite("sapo.png", self.img)
        
    def add_to_canvas(self, x, y, intensity):
        h = self.side * intensity
        if y in self.canvas_r:
            self.canvas_r[y]["x"].append(x)
            self.canvas_r[y]["height"].append(h)
        else:
            self.canvas_r[y] = {}
            self.canvas_r[y]["x"] = [x]
            self.canvas_r[y]["height"] = [h]
    
    def out_of_bounds(self, point):
        return (point[0] < 0) or (point[0] > self.width) or (point[1] < 0) or (point[1] > self.height)

    def quadrant(self, h_sign, v_sign):
        move_h_r        = self.r.dot( np.array([self.kernel_s,0]) ) # move horizontally rotated
        move_v_r        = self.r.dot( np.array([0,self.kernel_s]) ) # move vertically rotated
        vertices        = np.array([[0, 0,                      h_sign*self.kernel_s,  h_sign*self.kernel_s], 
                                    [0, v_sign*self.kernel_s,   v_sign*self.kernel_s,  0]])
        vertices_r      = self.r.dot(vertices).T + np.array([self.x_center, self.y_center])
        for y in range(int(1e10)):
            for x in range(int(1e10)):
                current = vertices_r + x*h_sign*move_h_r + y*v_sign*move_v_r
                sel, slide_line = self.select_square(current)
                if not np.any(sel):
                    i1 = self.diagonal1.intersection(slide_line)
                    i2 = self.diagonal2.intersection(slide_line)
                    if( (i1 and not self.out_of_bounds(i1) and slide_line.at(i1[0]) > h_sign*current[0][0])
                     or (i2 and not self.out_of_bounds(i2) and slide_line.at(i2[0]) > h_sign*current[0][0])):
                        continue
                    else: break
                self.add_to_canvas( h_sign*(self.side/2 + x*self.side),
                                    v_sign*(self.side/2 + y*self.side),
                                    get_intensity(self.img[sel]))
                self.img[sel] = self.color
                self.color = (50 if self.c%2==0 else 20)+[50,100][(h_sign+1)//2]+[50,100][(v_sign+1)//2]
                self.c += 1
            if x == 0: break
            
    def draw_canvas(self):
        bg_color    = (255, 255, 255)
        fg_color    = (0, 0, 0)
        img_out     = Image.new("RGB", (10000, 10000), bg_color)
        draw        = ImageDraw.Draw(img_out)
        self.canvas_r = dict(sorted(self.canvas_r.items()))
        c = 0
        ro = rotation_matrix(-self.angle)
        for y in self.canvas_r:
            line    = SigmoidPolygon(c*self.side, self.side, alpha = 1, N = 2)
            x       = np.array(self.canvas_r[y]["x"])
            i_sort  = np.argsort(x)
            x       = x[i_sort]
            height  = np.array(self.canvas_r[y]["height"])[i_sort]
            # min_ = min(x)
            for i in range(len(x)):
                line.height(i, height[i])
            line.compute_points()
            # print(y, len(x))
            # print(x)
            # print(height)
            # print(line.points)
            # print()
            # print("------------------------------------------------")
            # print()
            for i in range(len(line.points)):
                line.points[i] = tuple(self.r.dot(line.points[i])+[-min(x),0])
            line.draw(draw)
            c += 1
        img_out.save("5-out.png")
            

if __name__ == "__main__":
    kernel_s        = 23
    side            = 40    # size of the side of each square in the output img
    angle           = 45
    alpha           = 2
    img_name        = "5.jpg"
    img 		    = cv2.imread(img_name, cv2.IMREAD_GRAYSCALE)
    height, width   = img.shape
    scan            = Scan(img, kernel_s, side, angle)
    scan.scan()
    scan.draw_canvas()
    
    
    
