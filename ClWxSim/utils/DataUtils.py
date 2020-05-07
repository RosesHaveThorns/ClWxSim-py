import numpy as np

class DataUtils:
    """A collection of utility functions for handling data and variables"""

    @staticmethod
    def swap(world):
        temp = np.zeros((len(world.air_pressure), len(world.air_pressure)))

        for i in range(len(world.air_pressure)):
            for j in range(len(world.air_pressure)):
                temp[i][j] = world.old_air_pressure[i][j]

        for i in range(len(world.air_pressure)):
            for j in range(len(world.air_pressure)):
                world.old_air_pressure[i][j] = world.air_pressure[i][j]

        for i in range(len(world.air_pressure)):
            for j in range(len(world.air_pressure)):
                world.air_pressure[i][j] = temp[i][j]

        return world
