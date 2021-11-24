from PIL import Image, ImageDraw
import cv2
from bezier import Polygon
import numpy as np

def get_intensity(square):
    return 1-square.mean()/255
    

if __name__ == "__main__":
    kernel_s        = 23
    side            = 20    # size of the side of each square in the output img
    bg_color        = (255, 255, 255)
    fg_color        = (0, 0, 0)
    img_name        = "girl.jpg"
    img 		    = cv2.imread(img_name, cv2.IMREAD_GRAYSCALE)
    height, width   = img.shape
    n_row           = height // kernel_s # number of squares in the output img per row
    n_col           = height // kernel_s # number of squares in the output img per column
    img_out         = Image.new("RGB", (n_row*side, n_col*side), bg_color)
    
    for y in range(n_col):
        line      = Polygon(y*side)
        intensity = get_intensity( img[y*kernel_s:(y+1)*kernel_s, 0:kernel_s] )
        height    = intensity*side
        y_top     = (side-height)//2
        y_bot     = height + y_top
        line.extend([(0,y_bot), (0,y_top)])
        line.extend_bottom((side//2,y_bot))
        line.extend_top((side//2,y_top))
        for x in range(1,n_row-1):
            intensity   = get_intensity( img[y*kernel_s:(y+1)*kernel_s, x*kernel_s:(x+1)*kernel_s] )
            height      = intensity*side
            y_top     = (side-height)//2
            y_bot     = height + y_top
            line.extend_bottom((side//2 + x*side,y_bot))
            line.extend_top((side//2 + x*side,y_top))
        # TODO
        intensity   = get_intensity( img[y*kernel_s:(y+1)*kernel_s, x*kernel_s:(x+1)*kernel_s] )
        height      = intensity*side
        y_top     = (side-height)//2
        y_bot     = height + y_top
        line.extend_bottom((side//2 + x*side,y_bot))
        line.extend_top((side//2 + x*side,y_top))
        line.extend([(0,y_bot), (0,y_top)])
            
    # im      = Image.new("RGB", (200, 100), (255, 255, 255)) 
    # draw    = ImageDraw.Draw(im)
    # p       = Polygon(100)
    # 
    # p.extend([(0,80), (0,20)])
    # p.extend([(0,20), (50,25), (150,40), (199,35)])
    # p.extend([(199,35), (199,65)])
    # p.extend([(0,80), (50,75), (150,60), (199,65)][::-1])
    # 
    # p.draw(draw)
    # 
    # # draw.ellipse((0,20,1,21), fill = "black")
    # # draw.ellipse((50,25,51,26), fill = "black")
    # # draw.ellipse((150,40,151,41), fill = "black")
    # # draw.ellipse((199,35,200,36), fill = "black")
    # # 
    # # draw.ellipse((0,80,1,81), fill = "black")
    # # draw.ellipse((50,75,51,76), fill = "black")
    # # draw.ellipse((150,60,151,61), fill = "black")
    # # draw.ellipse((199,65,200,66), fill = "black")
    # im.save("out.png")
