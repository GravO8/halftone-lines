import cv2
import numpy as np

def rotation_matrix(angle):
    angle = np.deg2rad(angle)
    return np.array([[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]])
    
def make_edge(a, b):
    slope       = (a[1]-b[1])/(a[0]-b[0])
    intercept   = a[1] - slope*a[0]
    return slope, intercept
    
def make_edges(vertices):
    '''
    Outputs the four edges of the tilted square. Two parallel sides at the time.
    '''
    edges = []
    edges.append( make_edge(vertices[0],vertices[1]) )
    edges.append( make_edge(vertices[2],vertices[3]) )
    edges.append( make_edge(vertices[1],vertices[2]) )
    edges.append( make_edge(vertices[-1],vertices[0]) )
    assert edges[0][0]-edges[1][0] < 1e-5, "first two edges aren't parallel"
    assert edges[2][0]-edges[3][0] < 1e-5, "last two edges aren't parallel"
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
    b01, b11    = edges[0][1], edges[1][1]
    b21, b31    = edges[2][1], edges[3][1]
    slope0      = edges[0][0]
    slope1      = edges[2][0]
    cond0       = lambda x,y: slope0*x + min(b01,b11) <= y <= slope0*x + max(b01,b11)
    cond1       = lambda x,y: slope1*x + min(b21,b31) <= y <= slope1*x + max(b21,b31)
    return cond0, cond1
    

class Scan:
    def __init__(self, img, kernel_s, angle):
        self.img        = img
        self.height     = self.img.shape[0]
        self.width      = self.img.shape[1]
        self.x_center   = self.width//2
        self.y_center   = self.height//2
        self.kernel_s   = kernel_s
        self.angle      = angle
        self.selection  = np.zeros((self.width,self.height), dtype = bool)
    
    def select_square(self, vertices):
        edges                       = make_edges(vertices)
        cond0, cond1                = make_conds(edges)
        sel                         = np.array(self.selection, copy = True)
        min_x, min_y, max_x, max_y  = make_bbox(vertices)
        print(self.width)
        print(self.height)
        print(sel.shape)
        for x in range(max(0,min_x), min(max_x,self.width)):
            for y in range(max(0,min_y), min(max_y,self.height)):
                sel[x][y] = cond0(x,y) and cond1(x,y)
        return sel

    def third_quadrant(self):
        r               = rotation_matrix(self.angle)
        vertices        = np.array([[0, 0,              self.kernel_s,  self.kernel_s], 
                                    [0, self.kernel_s,  self.kernel_s,  0]])
        vertices_r      = r.dot(vertices).T + np.array([self.x_center, self.y_center])
        # move_right      = np.array([self.kernel_s,0])
        # move_up         = np.array([0,self.kernel_s])
        # move_right_r    = move_right.dot(r)
        # move_up_r       = move_up.dot(r)
        sel             = self.select_square(vertices_r).T
        self.img[sel]   = 0
        cv2.imwrite("sapo.png", img)

if __name__ == "__main__":
    kernel_s        = 99
    side            = 40    # size of the side of each square in the output img
    img_name        = "5.jpg"
    img 		    = cv2.imread(img_name, cv2.IMREAD_GRAYSCALE)
    height, width   = img.shape
    angle           = 20
    scan            = Scan(img, kernel_s, angle)
    scan.third_quadrant()
    
    
    
