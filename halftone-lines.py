from PIL import Image, ImageDraw
import cv2
from bezier import Polygon
import numpy as np

def get_intensity(square):
    return 1-square.mean()/255
    

if __name__ == "__main__":
    kernel_s        = 23
    img_name        = "girl.jpg"
    img 		    = cv2.imread(img_name, cv2.IMREAD_GRAYSCALE)
    height, width   = img.shape
    
    for y in range(0, height, kernel_s):
        for x in range(0, width, kernel_s):
            intensity = get_intensity( img[y:y+kernel_s, x:x+kernel_s] )
            
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
