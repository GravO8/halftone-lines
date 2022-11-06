# Halftone Lines

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

## 3. Drawing

While scanning, the position of the different image regions visited and their respective mean grey level intensity are stored in a dictionary, indexed by the region's `y` position (variable `self.canvas_r`).

