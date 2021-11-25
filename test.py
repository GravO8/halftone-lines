from PIL import Image, ImageDraw
import cv2
from bezier import Polygon
import numpy as np

def get_intensity(square):
    return 1-square.mean()/255
    
def get_rectangle(y, x, section):
    rectangle = Polygon(y*side)
    intensity = get_intensity( section )
    height    = intensity*side
    y_top     = (side-height)//2
    y_bot     = height + y_top
    rectangle.extend([(x*side,y_bot), (x*side,y_top)])
    rectangle.extend([(x*side,y_top), ((x+1)*side,y_top)])
    rectangle.extend([((x+1)*side,y_top), ((x+1)*side,y_bot)])
    rectangle.extend([((x+1)*side,y_bot, x*side,y_bot)])
    return rectangle
    

if __name__ == "__main__":
    kernel_s        = 23
    side            = 40    # size of the side of each square in the output img
    bg_color        = (255, 255, 255)
    fg_color        = (0, 0, 0)
    img_name        = "girl.jpg"
    img 		    = cv2.imread(img_name, cv2.IMREAD_GRAYSCALE)
    height, width   = img.shape
    n_row           = width // kernel_s  # number of squares in the output img per row
    n_col           = height // kernel_s # number of squares in the output img per column
    img_out         = Image.new("RGB", (n_row*side, n_col*side), bg_color)
    draw            = ImageDraw.Draw(img_out)
    
    for y in range(n_col):
        for x in range(n_row):
            r = get_rectangle(y, x, img[y*kernel_s:(y+1)*kernel_s, x*kernel_s:(x+1)*kernel_s])
            r.draw(draw)
    img_out.save("out.png")
