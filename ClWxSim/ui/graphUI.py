import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import keyboard

import ClWxSim.sim.world.World
import ClWxSim.sim.controller.Controller as Control

from ClWxSim.utils.logging import Logger

def startHeatmap(axar, array1, array2, array3):
    im0 = axar[0].imshow(array1, cmap='hot')
    axar[0].set_title('pressure Map')
    plt.colorbar(im0, ax=axarr[0])

    im1 = axar[1].imshow(array2, cmap='hot')
    axar[1].set_title('vel_u Map')
    plt.colorbar(im1, ax=axarr[1])

    im2 = axar[2].imshow(array3, cmap='hot')
    axar[2].set_title('vel_v Map')
    plt.colorbar(im2, ax=axarr[2])


    plt.pause(0.01)

def loadHeatmap(axar, array1, array2, array3):
    axar[0].imshow(array1, cmap='hot')
    axar[0].set_title('pressure Map')

    axar[1].imshow(array2, cmap='hot')
    axar[1].set_title('wind u velocity Map')

    axar[2].imshow(array3, cmap='hot')
    axar[2].set_title('wind v velocity Map')

    plt.pause(0.01)

if __name__ == "__main__":
    logger = Logger(log_name="ui")

    test_wld = World(world_name="test_world", wld_grid_size=100, starting_pressure=0.0)
    sim = Control(test_wld)

    test_wld.clear_data()

    logger.log("World and Controller ready")

    plt.ion()
    fig, axarr = plt.subplots(3,1)

    logger.log("Pyplot ready, beggining sim")

    startHeatmap(axarr, pressure, vel_u, vel_v)

    sim.running = True

    while !keyboard.is_pressed('x'):
        try:
            sim.tick()
        except Exception as e:
            logger.log("Error during tick {}: [{}]".format(sim.tickNum, e))

        if keyboard.is_pressed('s'):
            loadHeatmap(axarr, pressure, vel_u, vel_v)
            logger.log("Showing data for tick {}".format(sim.tickNum))
        elif sim.tickNum % 100 == 0:
            logger.log("Reached tick {}".format(sim.tickNum))

    sim.running = False
