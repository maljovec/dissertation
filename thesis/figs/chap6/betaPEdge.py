import matplotlib.pyplot as plt
import numpy as np
import scipy.spatial.distance
import sklearn.metrics
import math

## Alter the grid resolution
dx = 0.01
dy = 0.01

## Alter the line segment's endpoints
xls = 0.5*np.array([-1,1])

## Alter the line segment's orientation and offset
m = -0.5
b = 0
theta = -math.atan2(m,1)
sT = np.sin(theta)
cT = np.cos(theta)

def line(x):
    return m*x + b

def pNorm(p,x,y):
    return np.linalg.norm(x-y,ord=p)
    # return np.power(np.sum(np.power(np.abs(x-y),p)),1./p)

## Just do the Gabriel graph for easing the math
cx = np.average(xls)
cy = line(cx)
center = np.array([cx, cy])


def pNormToPoint(p,x):
    x = np.array([cT*x[0] - sT*x[1], sT*x[0] + cT*x[1]])
    return pNorm(p,x,center)

## Generate 2 2d grids for the x & y bounds
y, x = np.mgrid[slice(-1, 1 + dy, dy),
                slice(-1, 1 + dx, dx)]

## Then flatten x and y coordinates together for easy processing
points = np.vstack((x.flatten(),y.flatten())).T

pltCount = 1
pValues = [0.25,0.5,1,2,5,np.inf]

p0 = np.array( [xls[0], line(xls[0])] )
p1 = np.array( [xls[1], line(xls[1])] )

for p in pValues:

    ## Alter the displayed contours here
    r0 = np.array([cT*p0[0] - sT*p0[1] + cx, sT*p0[0] + cT*p0[1] + cy])
    ## Verify that these values are the same
    # r1 = np.array([cT*p1[0] - sT*p1[1] + cx, sT*p1[0] + cT*p1[1] + cy])
    # print(pNorm(p,r0,center),pNorm(p,r1,center))

    levels = [pNorm(p,r0,center)]

    z = np.zeros(len(points))
    for i,pi in enumerate(points):
        z[i] = pNormToPoint(p,pi)
    z = z.reshape(x.shape)

    z_min = min(0,z.min())
    z_max = max(1,z.max())

    plt.subplot(2,(len(pValues)+1)/2,pltCount)
    plt.pcolor(x, y, z, cmap='binary', vmin=z_min, vmax=z_max)
    plt.contour(x, y, z, colors='k', levels=levels, linestyles='dashed')
    plt.plot(xls,line(xls),c='k', marker='o')
    plt.title(r'$p = {}$'.format('\infty' if np.isinf(p) else p))
    # set the limits of the plot to the limits of the data
    plt.axis([x.min(), x.max(), y.min(), y.max()])
    plt.gca().set_aspect('equal')
    plt.gca().set_yticks([])
    plt.gca().set_xticks([])
    # plt.colorbar()

    pltCount += 1

plt.show()