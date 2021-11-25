from PIL import Image, ImageDraw
from sigmoid import SigmoidPolygon
import numpy as np
import cv2

def get_intensity(square):
    return 1-square.mean()/255
    

if __name__ == "__main__":
    kernel_s        = 23
    side            = 40    # size of the side of each square in the output img
    bg_color        = (255, 255, 255)
    fg_color        = (0, 0, 0)
    img_name        = "5.jpg"
    img 		    = cv2.imread(img_name, cv2.IMREAD_GRAYSCALE)
    height, width   = img.shape
    n_row           = width // kernel_s  # number of squares in the output img per row
    n_col           = height // kernel_s # number of squares in the output img per column
    img_out         = Image.new("RGB", (n_row*side, n_col*side), bg_color)
    draw            = ImageDraw.Draw(img_out)
    print(height, width)
    print(n_row, n_col, n_row*n_col)
    
    for y in range(n_col):
        line = SigmoidPolygon(y*side, side, slope = 0.0000001, N = 20)
        for x in range(1,n_row-1):
            intensity = get_intensity( img[y*kernel_s:(y+1)*kernel_s, x*kernel_s:(x+1)*kernel_s] )
            height    = intensity*side
            line.height(x*side, height)
        line.draw(draw)
        # break
    img_out.save("out.png")
