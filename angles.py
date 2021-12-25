import numpy as np
import matplotlib.pyplot as plt

x = np.arange(-100,100,200)

def rotation_matrix(angle):
    angle = np.deg2rad(angle)
    return np.array([[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]])
    
plt.figure(figsize = [5,5])
plt.axvline(0)
plt.axhline(0)
plt.axis("equal")
plt.grid(True)
x = np.array([0,1])
x1 = np.array([-0.34202014, 0.93969262])
plt.scatter(x[0],x[1], color = "purple")
plt.scatter(x1[0],x1[1], color = "red")
plt.show()

# print( np.tan(np.deg2rad(0)) )
