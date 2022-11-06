# Halftone Lines

A python script that levarages the [open cv](https://docs.opencv.org/master/index.html) and [PIL](https://pillow.readthedocs.io/en/stable/) libraries to generate halftone images, with lines.

*(If you like this repo, you may also like [this one](https://github.com/GravO8/halftone))*



## Command line usage

Put the source image in the same directory as `halftone_lines_cmd.py` and execute the script from the command line, like so:

```
python3 halftone_lines_cmd.py landscape.jpg
```

![example](https://user-images.githubusercontent.com/25433159/200199025-ca88002c-585b-4741-8602-48acc8ce5291.png)

You can also learn about the [optional arguments](https://github.com/GravO8/halftone#optional-arguments), doing so:

 ````
 python3 halftone_lines_cmd.py -h
 ````

**Warning**: The script takes a long time to execute for large images. Consider resizing the input image so that neither the height nor the width is larger than 1000 pixels.



## Optional arguments

### Kernel Size

As described in the [algorithm section bellow](#algorithm), the image is scanned with a (squared) kernel in a sliding window fashion. You can control the size of this kernel with the `kernel` optional argument. 

![kernel](https://user-images.githubusercontent.com/25433159/200199320-0f81db35-5159-4423-a6ae-506d0d68ef3c.png)

Larger kernels scan larger chunks of the image at a time, resulting in courser output images. Using smaller kernels results in smoother images but takes longer and produces larger outputs.

### Side

The `side` optional argument controls the size of the lines in the output image.

![side](https://user-images.githubusercontent.com/25433159/200199701-4f382665-3f77-44ad-b4fc-7982535484ae.png)

Larger `side` values produce smoother but also larger output images. Smaller `side` values generate smaller images with interesting textures.

### Alpha

When `alpha = 1`, the maximum width of each line is the `side` value. The `alpha` argument can be used to decrease or increase this maximum width using values less than or larger than 1, respectively. 

![alpha](https://user-images.githubusercontent.com/25433159/200199788-55e55c84-7353-4cb2-9a27-e7dd51a0fee5.png)

### Angle

The `angle` optional parameter controls the angle the image is scanned, which is then reflected on the output image like so:

![angle](https://user-images.githubusercontent.com/25433159/200199914-af443402-3545-4798-aeec-86e2b8061f15.png)

You can specify any angle you want, in degrees. The angle is pushed into the [0, 180[ range (which includes all possible rotation variations) before being applied to the image. 

### Color

The `bg_color` and `fg_color` optional arguments set the background and foreground colors of the output image, respectively.

![color](https://user-images.githubusercontent.com/25433159/200200030-ed2e1679-5cdd-462f-beb1-d080f81e7c84.png)

Darker colors are recommended for the foreground color. If you are calling the program using the command line interface, you have to use `""` or `''` to delimit the rgb value, like so:

 ```
 python3 halftone_lines_cmd.py landscape.jpg -fg "(255,0,0)"
 ```



## Algorithm

The algorithm is composed of two parts: the scanning and the drawing. In the scanning part, a sliding window kernel computes the mean grey level intensity of every image region it visits. Then, in the drawing part, lines whose thickness varies depending on the intensities previously measured, are drawn.

### 1. The Kernel and the Quadrants

The algorithm scans the input image in its four quadrants. This is done by finding the center of the image (variable `self.center`) and placing four squared kernels there, like so:
```
   +-------+      +-------+      +-------+
   |       |      |       |      | +-+-+ |    
   |       |      |   o   |      | +-o-+ |        
   |       |      |       |      | +-+-+ |        
   +-------+      +-------+      +-------+
   input img      input img   the four squares   
                  center      around the center
```
These kernels are defined by the array `vertices` in the `quadrant` method of the [`Scan` class](https://github.com/GravO8/halftone-lines/blob/master/scan.py). They are constructed from the base kernel defined by the vertices `(0,0)`, `(0,self.kernel_s)`, `(self.kernel_s,self.kernel_s)` and `(self.kernel_s,0)`, where `kernel_s` stands for *"kernel side"*. 

The arguments `h_sign` and `v_sign` (horizontal and vertical sign, respectively) are used to diferentiate four kernels (and quadrants):
```
(h_sign = +1) and (v_sign = +1) is the fourth quadrant (bottom right)
(h_sign = -1) and (v_sign = +1) is the second quadrant (bottom left)
(h_sign = -1) and (v_sign = -1) is the second quadrant (top left)
(h_sign = +1) and (v_sign = -1) is the first quadrant (top right)
```
Note: This may seen unintuitive when compared to the [mathematical description](https://p.tutorme.click/media/8c8c4f25a61c0551b6825e7ba45f573a.png) of the four quadrants. However, we have to consider that unlike in the mathematical coordinate system, where the point (0,0) is the center of the coordinate space, the point (0,0) in a 2D matrix (an image) is the upper left corner. Additionally, increasing y coordinates move down along the matrix, not up.

The kernel's vertices are then rotated by `angle` degrees using the rotation matrix generated by the `rotation_matrix` function and moved to the center of the image by adding the center coordinates:
```python
vertices_r = self.r.dot(vertices).T + self.center
```
### 2. Sliding Window

Ok, the kernels are in place. How can they be moved to scan the image? This is done with translation vectors, the `move_h_r` and `move_v_r` variables, that move the kernels horizontally and vertically, respectively and are defined like so:

```python
move_h_r = self.r.dot( np.array([self.kernel_s,0]) ) # move horizontally rotated
move_v_r = self.r.dot( np.array([0,self.kernel_s]) ) # move vertically rotated
```

They too are rotated by `angle` degrees to match the orientation of the kernels. 

The current position of the kernel is updated like so:

```
current = vertices_r + x*h_sign*move_h_r + y*v_sign*move_v_r
```

Where `x` and `y` are integer values that range from 0 to an artibitrarly large number. This means the kernel can move to places outside the original image. Indeed, when the kernel reaches a position outside the image, its sliding movement is stopped.

The image below has a schematic representation of how the sliding window works. Colored squares represent places the kernel visits in the third quadrant. Green squares represent squares where the kernel is used to compute the underlying grey level intensity mean. As long as the kernel overlaps with the image with at least one pixel, its mean will be considered. Red squares are the last position visited by the scanning algorithm in each row. As depicted by the numbers, which correspond to the `x` values of that particular row, the kernel in this quadrant moves from left to right. In this case, red squares are squares outside the image and where continuing moving left won't ever reach the image.The yellow squares are also outside the image, but on the other hand, continuing moving left from their position can reach the image. The `x` iteration stops in the red squares. The `y` iretation stops in the last red square, corresponding to the last row where no pixel in the image is scan because the row is completely outside the image bounding box.

<img src="https://user-images.githubusercontent.com/25433159/199332249-c589dd6c-0337-4814-845f-74821e123cd7.png" alt="sliding window corner" style="zoom:24%;" />

Note: The algorithm can be optimized by directly updating the `StraightLine` objects instead of constructing new objects everytime the kernel is moved.

### 3. Drawing

While scanning, the position of the different image regions visited and their respective mean grey level intensity are stored in a dictionary, indexed by the region's `y` position (variable `self.canvas_r`). The output image is created by iterating this dictionary as each of its entries corresponds to a line. The lines are created with the `SigmoidPolygon` class that, as the name suggests, creates the polygons that are then actually drawn. The points in this line are added with the `height` method that specifies the thickness (or height) the line should have at a particular position. The smooth thickness variation is implemented with a sigmoid function (see the `make_sigmoid` method). As the lines are drawn tilted (following the kernel's orientation), they must be rotated to match the original orientation by reverting the `angle` degrees rotation and finally, they are translatated to the center of the image.



## Original image credits

The photo used in this README is called **Landscape with Mountains and Small Pond** and you can see the original version [here](https://www.pexels.com/photo/landscape-with-mountains-and-small-pond-12365658/). Check out its original photographer [here](https://www.pexels.com/@eberhardgross/).



## License

This program is licensed under the MIT License - see the [LICENSE](https://github.com/GravO8/halftone-lines/blob/master/LICENSE) file for details.
