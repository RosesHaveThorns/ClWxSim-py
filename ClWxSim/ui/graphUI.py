import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import keyboard

from ClWxSim.data.world import World
from ClWxSim.sim.controller import Controller as Control

import ClWxSim.sim.fluid_solver as solver

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
    logger = Logger(log_ID="ui")

    wld = World(world_name="world", wld_grid_size=100, starting_pressure=0.0)
    sim = Control(wld)

    wld.clear_data()

    logger.log("World and Controller ready")

    plt.ion()
    fig, axarr = plt.subplots(3,1)

    logger.log("Pyplot ready, beggining sim")

    # Add test sources
    added_p_grid = np.zeros((wld.grid_size, wld.grid_size))
    added_p_grid[20,50] = 10.
    added_p_grid[20-1,50] = 10.
    added_p_grid[20+1,50] = 10.
    added_p_grid[20,50-1] = 10.
    added_p_grid[20,50+1] = 10.

    added_u_grid = np.zeros((wld.grid_size, wld.grid_size))
    added_u_grid[20,50] = 15.
    added_u_grid[7,12] = -15.
    added_u_grid[70,80] = 15.

    added_v_grid = np.zeros((wld.grid_size, wld.grid_size))
    added_v_grid[7,12] = 15.

    solver.add_source(wld.wld_grid_size, wld.air_pressure, added_p_grid, wld.dt)
    solver.add_source(wld.wld_grid_size, wld.air_vel_u, added_u_grid, wld.dt)
    solver.add_source(wld.wld_grid_size, wld.air_vel_v, added_v_grid, wld.dt)

    # Start ui
    startHeatmap(axarr, wld.air_pressure, wld.air_vel_u, wld.air_vel_v)

    # Run simulation
    sim.running = True

    while not keyboard.is_pressed('x'):
        try:
            sim.tick()
        except Exception as e:
            logger.log("Error during tick {}: [{}]".format(sim.tickNum, e))

        if keyboard.is_pressed('s'):
            loadHeatmap(axarr, wld.air_pressure, wld.air_vel_u, wld.air_vel_v)
            logger.log("Showing data for tick {}".format(sim.tickNum))

        elif sim.tickNum % 100 == 0:
            logger.log("Reached tick {}".format(sim.tickNum))

    sim.running = False
