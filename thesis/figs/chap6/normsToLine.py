import matplotlib.pyplot as plt
import numpy as np
import scipy.spatial.distance
import sklearn.metrics

## Alter the grid resolution
dx = 0.05
dy = 0.05

## Alter the line segment's endpoints
xls = 0.5*np.array([-1,1])

## Alter the line segment's orientation and offset
m = -0.
b = 0

## Alter the displayed contours here
levels = [0.5]

def line(x):
    return m*x + b

def pNorm(p,x,y):
    return np.linalg.norm(x-y,ord=p)
    # return np.power(np.sum(np.power(np.abs(x-y),p)),1./p)

def pNormToLine(p,x):
    testVals = []
    for yx in np.linspace(xls[0],xls[1],101):
        yy = line(yx)
        testVals.append(pNorm(p,x,np.array([yx,yy])))
    return np.min(testVals)

## Generate 2 2d grids for the x & y bounds
y, x = np.mgrid[slice(-1, 1 + dy, dy),
                slice(-1, 1 + dx, dx)]

## Then flatten x and y coordinates together for easy processing
points = np.vstack((x.flatten(),y.flatten())).T

pValues = [0.25,0.5,1,2,5,np.inf]

fig, axes = plt.subplots(2,(len(pValues)+1)/2)

Zs = []
for p,ax in zip(pValues,axes.reshape(-1)):
    z = np.zeros(len(points))
    for i,pi in enumerate(points):
        z[i] = pNormToLine(p,pi)
    z = z.reshape(x.shape)
    Zs.append(z)

    z_min = min(0,z.min())
    z_max = max(1,z.max())

    ax.pcolor(x, y, z, cmap='binary', vmin=z_min, vmax=z_max)
    ax.plot(xls,line(xls),c='k', marker='o')
    plt.title(r'$p = {}$'.format('\infty' if np.isinf(p) else p))
    # set the limits of the plot to the limits of the data
    plt.axis([x.min(), x.max(), y.min(), y.max()])
    ax.set_aspect('equal')
    ax.set_yticks([])
    ax.set_xticks([])
    # plt.colorbar()

for ax in axes.reshape(-1):
    for z in Zs:
        ax.contour(x, y, z, colors='#ffffff', levels=levels, linestyles='dashed')

plt.show()