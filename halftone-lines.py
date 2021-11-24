from PIL import Image
from PIL import ImageDraw
from bezier import Polygon


if __name__ == "__main__":
    im      = Image.new("RGB", (200, 100), (255, 255, 255)) 
    draw    = ImageDraw.Draw(im)
    p       = Polygon(100)
    
    p.extend([(0,80), (0,20)])
    p.extend([(0,20), (50,25), (150,40), (199,35)])
    p.extend([(199,35), (199,65)])
    p.extend([(0,80), (50,75), (150,60), (199,65)][::-1])

    p.draw(draw)
    
    # draw.ellipse((0,20,1,21), fill = "black")
    # draw.ellipse((50,25,51,26), fill = "black")
    # draw.ellipse((150,40,151,41), fill = "black")
    # draw.ellipse((199,35,200,36), fill = "black")
    # 
    # draw.ellipse((0,80,1,81), fill = "black")
    # draw.ellipse((50,75,51,76), fill = "black")
    # draw.ellipse((150,60,151,61), fill = "black")
    # draw.ellipse((199,65,200,66), fill = "black")
    im.save("out.png")
