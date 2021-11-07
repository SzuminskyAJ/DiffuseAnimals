import random
import numpy as np
from matplotlib import pyplot as plt
import imageio
import os

steps = 10000
size = 150
filenames = []

Du = 0.16
Dv = 0.08
F = 0.020
k = 0.055

def laplacian(Z):
    Ztop = Z[0:-2, 1:-1]
    Zleft = Z[1:-1, 0:-2]
    Zbottom = Z[2:, 1:-1]
    Zright = Z[1:-1, 2:]
    Zcenter = Z[1:-1, 1:-1]
    return (Ztop + Zleft + Zbottom + Zright -
            4 * Zcenter)


'''U = np.empty(shape=(width+2,height+2))
U.fill(0)
V = np.empty(shape=(width+2,height+2))
V.fill(0)
u = np.random.random((width,height))
v = np.random.random((width,height))'''


Z = np.zeros((size+2,size+2), [('U', np.double), ('V', np.double)])
U,V = Z['U'], Z['V']
u,v = U[1:-1,1:-1], V[1:-1,1:-1]

print(v.shape)


r = 20
u[...] = 1.0
U[int(size/2-r):int(size/2+r),int(size/2-r):int(size/2+r)] = 0.50
V[int(size/2-r):int(size/2+r),int(size/2-r):int(size/2+r)] = 0.25
u += 0.05*np.random.random((size,size))
v += 0.05*np.random.random((size,size))



p = 0
for i in range(steps):
    Lu = laplacian(U)
    Lv = laplacian(V)
    u += (Du*Lu - (u*v*v) + F *(1-u))
    v += (Dv*Lv + (u*v*v) - (F+k)*v)

    # Neumann conditions: derivatives at the edges
    # are null.
    for Z in (U, V):
        Z[0, :] = Z[1, :]
        Z[-1, :] = Z[-2, :]
        Z[:, 0] = Z[:, 1]
        Z[:, -1] = Z[:, -2]

    if i%500==0:
        plt.imshow(u, interpolation='nearest')
        plt.axis("off")
        plt.savefig(str(i)+'.png')
        filenames.append(str(i)+'.png')

with imageio.get_writer('mygif.gif', mode='I') as writer:
    for filename in filenames:
        image = imageio.imread(filename)
        writer.append_data(image)

for filename in set(filenames):
    os.remove(filename)
