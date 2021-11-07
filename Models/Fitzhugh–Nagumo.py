#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
from initial_states import *

# params
a = 0.0005
b = 0.005
tau = 0.1
k = 0

# sigma and lambda
L = 1
s = 1

# discretize time and space
size = 100  # size of the 2D grid
dx = 2. / size  # space step

T = 50  # total time
dt = .001  # time step
n = int(T / dt)  # number of iterations -- same as ryan's number of steps!

# initial state of concentration of both chemicals
#V = (~create_circular_mask(size, size, radius=size//4))
U = np.ones((size, size))
V = np.ones((size, size))

U_noise = np.random.rand(size, size)
V_noise = np.random.rand(size, size)

U += 0.0001*U_noise
V += 0.0001*V_noise

# helper fct
def laplacian(Z):
    Ztop = Z[0:-2, 1:-1]
    Zleft = Z[1:-1, 0:-2]
    Zbottom = Z[2:, 1:-1]
    Zright = Z[1:-1, 2:]
    Zcenter = Z[1:-1, 1:-1]
    return (Ztop + Zleft + Zbottom + Zright -
            4 * Zcenter) / dx**2

def show_patterns(U, ax=None):
    ax.imshow(U, cmap=plt.cm.viridis,
              interpolation='bilinear',
              extent=[-1, 1, -1, 1])
    ax.set_axis_off()


fig, axes = plt.subplots(3, 3, figsize=(8, 8))
step_plot = n // 9

# We simulate the PDE with the finite difference
# method.
for i in range(n):

    # We compute the Laplacian of u and v.
    deltaU = laplacian(U)
    deltaV = laplacian(V)

    # We take the values of u and v inside the grid.
    Uc = U[1:-1, 1:-1]
    Vc = V[1:-1, 1:-1]

    # We update the variables. -- this is the part that changed the most!
    U[1:-1, 1:-1] = Uc + dt * (a * deltaU + L*Uc - Uc**3 - k - s*(Vc))
    V[1:-1, 1:-1] = Vc + dt * (b * deltaV + Uc - Vc) / tau


    # Neumann conditions: derivatives at the edges
    # are null.
    for Z in (U, V):
        Z[0, :] = Z[1, :]
        Z[-1, :] = Z[-2, :]
        Z[:, 0] = Z[:, 1]
        Z[:, -1] = Z[:, -2]

    # We plot the state of the system at
    # 9 different times.
    if i % step_plot == 0 and i < 9 * step_plot:
        ax = axes.flat[i // step_plot]
        show_patterns(U, ax=ax)
        ax.set_title(f'$t={i * dt:.2f}$')


fig, ax = plt.subplots(1, 1, figsize=(8, 8))
show_patterns(U, ax=ax)

np.min(U)

np.min(V)
