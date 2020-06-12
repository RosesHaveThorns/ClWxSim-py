from ClWxSim.utils.logging import Logger
from ClWxSim.utils.DataUtils import DataUtils as dUtils
import numpy as np

class Pressure:
    """Contains functions required for Pressure grid calculations"""

    diff_rate = 0.0001

    def __init__(self):
        self.logger = Logger(log_name="pressure")

    def tick(self, world, dt):

        self.logger.log("Test world pressure BEFORE:\n{}\n".format(world.air_pressure))
        self.logger.log("Test world old pressure BEFORE:\n{}\n".format(world.old_air_pressure))

        #dUtils.swap(world)

        self.logger.log("Test world pressure BEFORE diffuse:\n{}\n".format(world.air_pressure))
        self.logger.log("Test world old pressure BEFORE diffuse:\n{}\n".format(world.old_air_pressure))

        self.diffuse(world, dt)

        ##dUtils.swap(world)

        self.logger.log("Test world pressure AFTER:\n{}\n".format(world.air_pressure))
        self.logger.log("Test world old pressure AFTER:\n{}\n".format(world.old_air_pressure))

        self.advect(world, dt)

        self.logger.log("Test world pressure AFTER:\n{}\n".format(world.air_pressure))
        self.logger.log("Test world old pressure AFTER:\n{}\n".format(world.old_air_pressure))
        self.logger.log("Pressure dt step simulated")
        return world

    def diffuse(self, world, dt):
        """Calculates the diffusion during time dt and returns the new air_pressure"""

        a = dt * self.diff_rate * world.grid_size * world.grid_size

        for k in range(20): # Iterate Guass-Seidel method 20 times

            for i in range(world.grid_size-1):  # Loop through all grid squares
                for j in range(world.grid_size-1):
                    world.air_pressure[i,j] = (world.old_air_pressure[i,j] + a * (world.air_pressure[i-1,j] + world.air_pressure[i+1,j] + world.air_pressure[i,j-1] + world.air_pressure[i,j+1])) / (1 + 4 * a)

        self.logger.log("Pressure diffusion calculated")

    def advect(self, world, dt):
        """Calculates the advection during time dt and returns the new air_pressure"""

        dt0 = dt * world.grid_size

        for i in range(world.grid_size):  # Loop through all grid squares
            x, y, i0, i1, j0, j1 = 0, 0, 0, 0, 0, 0

            for j in range(world.grid_size):
                x = i - dt0 * world.air_vectors[i,j][0]
                y = j - dt0 * world.air_vectors[i,j][1]

                if (x < 0.5):
                    x = 0.5

                if (x > world.grid_size + 0.5):
                    x = world.grid_size + 0.5
                    i0 = floor(x)
                    i1 = i0 + 1

                if (y < 0.5):
                    y = 0.5

                if (y > world.grid_size + 0.5):
                    y = world.grid_size + 0.5
                    j0 = floor(y)
                    j1 = j0 + 1

                s1 = x - i0
                s0 = 1 - s1
                t1 = y - j0
                t0 = 1 - t1

                world.air_pressure[i,j] = s0 * (t0 * world.old_air_pressure[i0,j0] + t1 * world.old_air_pressure[i0,j1]) + s1 * (t0 * world.old_air_pressure[i1,j0] + t1 * world.old_air_pressure[i1,j1])

        self.logger.log("Pressure advection calculated")
