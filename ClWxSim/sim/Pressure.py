from ClWxSim.utils.logging import Logger
from ClWxSim.utils.DataUtils import DataUtils as dUtils
import numpy as np

class Pressure:
    """Contains functions required for Pressure grid calculations"""

    diff_rate = 1

    def __init__(self):
        self.logger = Logger(log_name="pressure")

    def tick(self, world, dt):
        grid_size = world.grid_size
        air_pressure = world.air_pressure
        old_air_pressure = world.old_air_pressure
        air_vectors = world.air_vectors

        old_air_pressure, air_pressure = dUtils.swap(old_air_pressure, air_pressure)
        old_air_pressure, air_pressure = self.diffuse(grid_size, air_pressure, old_air_pressure, dt)
        old_air_pressure, air_pressure = dUtils.swap(old_air_pressure, air_pressure)
        old_air_pressure, air_pressure = self.advect(grid_size, air_pressure, old_air_pressure, air_vectors, dt)

        world.grid_size = grid_size
        world.air_pressure = air_pressure
        world.old_air_pressure = old_air_pressure
        world.air_vectors = air_vectors

        return world

        self.logger.log("Pressure dt step simulated")
        return world

    def diffuse(self, grid_size, air_pressure, old_air_pressure, dt):
        """Calculates the diffusion during time dt and returns the new air_pressure"""

        a = dt * self.diff_rate * grid_size * grid_size

        for k in range(20): # Iterate Guass-Seidel method 20 times

            for i in range(grid_size):  # Loop through all grid squares
                for j in range(grid_size):
                    air_pressure[i,j] = old_air_pressure[i,j] + a * (air_pressure[i-1,j] + air_pressure[i+1,j] + air_pressure[i,j-1] + air_pressure[i,j+1]) / (1 + 4 * a)

        self.logger.log("Pressure diffusion calculated")
        return old_air_pressure, air_pressure

    def advect(self, grid_size, air_pressure, old_air_pressure, air_vectors, dt):
        """Calculates the advection during time dt and returns the new air_pressure"""

        dt0 = dt * grid_size

        for i in range(grid_size):  # Loop through all grid squares
            for j in range(grid_size):
                x = i - dt0 * air_vectors[i,j][0]
                y = j - dt0 * air_vectors[i,j][1]

                if (x < 0.5):
                    x = 0.5

                if (x > grid_size + 0.5):
                    x = grid_size + 0.5
                    i0 = floor(x)
                    i1 = i0 + 1

                if (y < 0.5):
                    y = 0.5

                if (y > grid_size + 0.5):
                    y = grid_size + 0.5
                    j0 = floor(y)
                    j1 = j0 + 1

                s1 = x - i0
                s0 = 1 - s1
                t1 = y - j0
                t0 = 1 - t1

                air_pressure[i,j] = s0 * (t0 * old_air_pressure[i0,j0] + t1 * old_air_pressure[i0,j1]) + s1 * (t0 * old_air_pressure[i1,j0] + t1 * old_air_pressure[i1,j1]

        self.logger.log("Pressure advection calculated")
        return old_air_pressure, air_pressure
