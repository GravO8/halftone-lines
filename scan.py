import cv2
import numpy as np

def is_inside(width, height, edges):
    return 
    
def rotation_matrix(angle):
    angle = np.deg2rad(angle)
    return np.array([[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]])
    
def select_square(edges):
    

def first_quadrant(side, x_center, y_center, height, width):
    horizontal      = np.array([[i]*width for i in range(height)])
    vertical        = np.array([[i for i in range(width)]*height])
    r               = rotation_matrix(20)
    edges           = np.array([[[0,0],[0,kernel_s]],[[kernel_s,0],[kernel_s,kernel_s]]])
    edges_r         = edges.dot(r)
    move_right      = np.array([kernel_s,0])
    move_up         = np.array([0,kernel_s])
    move_right_r    = move_right.dot(r)
    move_up_r       = move_up.dot(r)
    

if __name__ == "__main__":
    kernel_s        = 18
    side            = 40    # size of the side of each square in the output img
    img_name        = "5.jpg"
    img 		    = cv2.imread(img_name, cv2.IMREAD_GRAYSCALE)
    height, width   = img.shape
    angle           = 20
    
    x_center = width//2
    y_center = height//2
    
    first_quadrant()
    
    
