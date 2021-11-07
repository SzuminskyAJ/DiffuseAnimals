import random
import numpy as np
from matplotlib import pyplot as plt
import imageio
import os

filenames = []

def laplacian(Z):
    Ztop = Z[0:-2, 1:-1]
    Zleft = Z[1:-1, 0:-2]
    Zbottom = Z[2:, 1:-1]
    Zright = Z[1:-1, 2:]
    Zcenter = Z[1:-1, 1:-1]
    return (Ztop + Zleft + Zbottom + Zright -
            4 * Zcenter)

def FitzHughModel(a,b,tau,k,L,s, size, n):

    dx = 2. / size
    dt = .001  # time step
    T = n * dt  # total time

    # initial state of concentration of both chemicals
    U = np.random.rand(size, size)
    V = np.random.rand(size, size)


    # Try a different initial state: circle
    def create_circular_mask(h, w, center=None, radius=None):
        """Returns a numpy array of the given size with all ones in a circle of given radius"""
        if center is None:  # use the middle of the image
            center = (int(w / 2), int(h / 2))
        if radius is None:  # use the smallest distance between the center and image walls
            radius = min(center[0], center[1], w - center[0], h - center[1])

        Y, X = np.ogrid[:h, :w]
        dist_from_center = np.sqrt((X - center[0]) ** 2 + (Y - center[1]) ** 2)

        mask = dist_from_center <= radius

        return mask.astype(int)


    # V = (~create_circular_mask(size, size, radius=size//4))
    U = np.ones((size, size))
    V = np.ones((size, size))

    U_noise = np.random.rand(size, size)
    V_noise = np.random.rand(size, size)

    U += 0.0001 * U_noise
    V += 0.0001 * V_noise


    # We simulate the PDE with the finite difference
    for i in range(n):

        # We compute the Laplacian of u and v.
        deltaU = laplacian(U)/ dx ** 2
        deltaV = laplacian(V)/ dx ** 2

        # We take the values of u and v inside the grid.
        Uc = U[1:-1, 1:-1]
        Vc = V[1:-1, 1:-1]

        # We update the variables. -- this is the part that changed the most!
        U[1:-1, 1:-1] = Uc + dt * (a * deltaU + L * Uc - Uc ** 3 - k - s * (Vc))
        V[1:-1, 1:-1] = Vc + dt * (b * deltaV + Uc - Vc) / tau

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

def GrayScottModel(diffusionRateA, diffusionRateB, Feed, Kill, Size, Steps):

    Z = np.zeros((Size+2,Size+2), [('U', np.double), ('V', np.double)])
    U,V = Z['U'], Z['V']
    u,v = U[1:-1,1:-1], V[1:-1,1:-1]


    #Add a square in the middle for the initial image
    u[...] = 1.0
    U[int(Size/2-20):int(Size/2+20),int(Size/2-20):int(Size/2+20)] = 0.50
    V[int(Size/2-20):int(Size/2+20),int(Size/2-20):int(Size/2+20)] = 0.25

    #Add random noise
    u += 0.05*np.random.random((Size,Size))
    v += 0.05*np.random.random((Size,Size))

    #Start applying the equations
    for i in range(Steps):
        Lu = laplacian(U)
        Lv = laplacian(V)
        u += (diffusionRateA*Lu - (u*v*v) + Feed *(1-u))
        v += (diffusionRateB*Lv + (u*v*v) - (Feed+Kill)*v)

        # Remove borders
        for Z in (U, V):
            Z[0, :] = Z[1, :]
            Z[-1, :] = Z[-2, :]
            Z[:, 0] = Z[:, 1]
            Z[:, -1] = Z[:, -2]

        #Save an image every 500 steps
        if i%500==0:
            plt.imshow(u, interpolation='nearest')
            plt.axis("off")
            plt.savefig(str(i)+'.png')
            filenames.append(str(i)+'.png')

    #Create and save a GIF with all of the images
    with imageio.get_writer('simulation.gif', mode='I') as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)

    #Delete old images
    for filename in set(filenames):
        os.remove(filename)

def simulateGif(Model, diffusionRateA, diffusionRateB, Feed, Kill, Size, Steps, Sigma, Lambda, Tau):
    """
        simulateGif returns a gif of a Reaction-Diffusion

        :param Model: One of the two model used (Gray-Scott / FitzHugh–Nagumo)
        :param diffusionRateA: Diffusion rate of A
        :param diffusionRateB: Diffusion rate of B
        :param Feed: Feed Variable
        :param Kill: Kill Variable
        :param Size: Size of the gif
        :param Steps: The number of times to run the equation
        :param Sigma: Sigma Variable
        :param Lambda: Lambda Variable
        :param Lambda: Tau Variable
    """

    if Model == "Gray-Scott":
        GrayScottModel(diffusionRateA, diffusionRateB, Feed, Kill, Size, Steps)
    elif Model == "FitzHugh–Nagumo":
        FitzHughModel(diffusionRateA, diffusionRateB, Tau, Kill, Lambda, Sigma, Size, Steps)



# *** Examples ***

#GrayScottModel(0.16, 0.08, 0.035, 0.060, 100, 10000)
#FitzHughModel(0.0005,0.005,0.1,0,1,1, 100, 10000)

#simulateGif("Gray-Scott", 0.16, 0.08, 0.035, 0.060, 256, 10000, 0,0,0)
#simulateGif("FitzHugh–Nagumo", 0.0005,0.005, 0, 0.060, 100, 10000, 1,1,0.1)