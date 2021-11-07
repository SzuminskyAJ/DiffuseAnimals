import random
import numpy as np
from matplotlib import pyplot as plt
import imageio
import os
import sys

filenames = []

def laplacian(Z):
    Ztop = Z[0:-2, 1:-1]
    Zleft = Z[1:-1, 0:-2]
    Zbottom = Z[2:, 1:-1]
    Zright = Z[1:-1, 2:]
    Zcenter = Z[1:-1, 1:-1]
    return (Ztop + Zleft + Zbottom + Zright -
            4 * Zcenter)

def initRandom(u, v, size):
    u[...] = 1.0
    v[...] = 1.0

def initCircle(u, v, size):
    # Try a different initial state: circle
    def create_circular_mask(h, w, radius=None):
        if radius is None:  # use the smallest distance between the center and image walls
            radius = min(center[0], center[1], w - center[0], h - center[1])

        Y, X = np.ogrid[:h, :w]
        dist_from_center = (X - w / 2) ** 2 + (Y - h / 2) ** 2

        return dist_from_center <= radius ** 2

    mask = create_circular_mask(size, size, radius=size//4)
    u += np.where(mask, 0.5, 1.0)
    v += np.where(mask, 0.25, 0.0)

def initSquare(u, v, size):
    #Add a square in the middle for the initial image
    u[...] = 1.0
    u[int(size/2-20):int(size/2+20),int(size/2-20):int(size/2+20)] = 0.50
    v[int(size/2-20):int(size/2+20),int(size/2-20):int(size/2+20)] = 0.25

def FitzHughModel(u, v, Lu, Lv, a, b, tau, k, L, s):
    dt = .001  # time step
    # We update the variables. -- this is the part that changed the most!
    u += dt * (a * Lu + L * u - u ** 3 - k - s * v)
    v += dt * (b * Lv + u - v) / tau

def GrayScottModel(u, v, Lu, Lv, diffusionRateA, diffusionRateB, Feed, Kill):
    u += (diffusionRateA*Lu - (u*v*v) + Feed *(1-u))
    v += (diffusionRateB*Lv + (u*v*v) - (Feed+Kill)*v)

def simulateGif(Model, InitialModel, diffusionRateA, diffusionRateB, noise, Size, Steps, Feed, Kill, Sigma, Lambda, Tau):
    """
        simulateGif returns a gif of a Reaction-Diffusion

        :param Model: One of the two model used (Gray-Scott / FitzHugh–Nagumo)
        :param InitialModel: One of the initial model used (Random, Square, Circle)
        :param diffusionRateA: Diffusion rate of A
        :param diffusionRateB: Diffusion rate of B
        :param noise: noise factor at start of simulation
        :param Size: Size of the gif
        :param Steps: The number of times to run the equation
        :param Feed: Feed Variable
        :param Kill: Kill Variable
        :param Sigma: Sigma Variable
        :param Lambda: Lambda Variable
        :param Tau: Tau Variable
    """

    # initial state of concentration of both chemicals
    U = np.zeros((Size + 2, Size + 2), dtype = np.float64)
    V = np.zeros((Size + 2, Size + 2), dtype = np.float64)
    # We take the values of u and v inside the grid.
    u = U[1:-1, 1:-1]
    v = V[1:-1, 1:-1]

    if InitialModel == "Square":
        initSquare(u, v, Size)
    elif InitialModel == "Random":
        initRandom(u, v, Size)
    elif InitialModel == "Circle":
        initCircle(u, v, Size)
    else:
        print('Unknown starting model')
        sys.exit(1)

    #Add random noise
    u += noise*np.random.random(u.shape)
    v += noise*np.random.random(v.shape)

    # We simulate the PDE with the finite difference
    for i in range(Steps):

        # We compute the Laplacian of u and v.
        Lu = laplacian(U)
        Lv = laplacian(V)

        # We update the variables. -- this is the part that changed the most!
        if Model == "Gray-Scott":
            GrayScottModel(u, v, Lu, Lv, diffusionRateA, diffusionRateB, Feed, Kill)
        elif Model == "FitzHugh–Nagumo":
            FitzHughModel(u, v, Lu, Lv, diffusionRateA, diffusionRateB, Tau, Kill, Lambda, Sigma)
        else:
            print('Unknown model')
            sys.exit(1)

        # Neumann conditions: derivatives at the edges
        # are null.
        for Z in (U, V):
            Z[0, :] = Z[1, :]
            Z[-1, :] = Z[-2, :]
            Z[:, 0] = Z[:, 1]
            Z[:, -1] = Z[:, -2]

        # Save an image every 500 steps
        if i % 500 == 0:
            plt.imshow(U, interpolation='nearest')
            plt.axis("off")
            plt.savefig(str(i) + '.png')
            filenames.append(str(i) + '.png')

    # Create and save a GIF with all of the images
    with imageio.get_writer('simulation.gif', mode='I') as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)

    # Delete old images
    for filename in set(filenames):
        os.remove(filename)

# *** Examples ***

#simulateGif("Gray-Scott", "Square", 0.16, 0.08, 0.05, 256, 10000, 0.035, 0.060, 0, 0, 0)
simulateGif("FitzHugh–Nagumo", "Circle", 0.0005 * 50**2, 0.005 * 50**2, 0.0001, 100, 10000, 0, 0.060, 1, 1, 0.1)
