from PIL import Image, ImageDraw
from sigmoid import SigmoidPolygon
import numpy as np
import cv2

def get_intensity(square):
    return 1-square.mean()/255
    

if __name__ == "__main__":
    kernel_s        = 18
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
    print(f"original size: {height}x{width}")
    print(f"new size: {n_col*side}x{n_row*side}")
    
    for y in range(n_col):
        line = SigmoidPolygon(y*side, side, alpha = 5, N = 2)
        for x in range(n_row):
            intensity = get_intensity( img[y*kernel_s:(y+1)*kernel_s, x*kernel_s:(x+1)*kernel_s] )
            height    = intensity*side
            line.height(x, height)
        line.draw(draw)
    # img_out = img_out.resize((n_row*side//2, n_col*side//2), resample = Image.ANTIALIAS)
    img_out.save(img_name+"-out.png")
