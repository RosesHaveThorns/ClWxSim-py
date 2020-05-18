import numpy as np

import matplotlib.pyplot as plt

import tkinter

import keyboard

from ClWxSim.data.world import World
from ClWxSim.sim.controller import Controller as Control

import ClWxSim.sim.fluid_solver as solver

from ClWxSim.utils.logging import Logger

cbar_arr = []


def startHeatmap(axar, array1, array2, array3, world):
    global im0, im1, im2, im3, im4
    im0 = axar[0,0].imshow(array1, cmap='hot')
    axar[0,0].set_title('Pressure (mbar) Map')
    plt.colorbar(im0, ax=axarr[0,0])

    full_grad_u, full_grad_v = world.calcPressureGrad(array1)

    im3 = axar[0,1].imshow(full_grad_u, cmap='Greys')
    axar[0,1].set_title('Pressure Gradient [u] Map')
    plt.colorbar(im3, ax=axarr[0,1])

    im4 = axar[0,2].imshow(full_grad_v, cmap='Greys')
    axar[0,2].set_title('Pressure Gradient [v] Map')
    plt.colorbar(im4, ax=axarr[0,2])

    im1 = axar[1,0].imshow(array2, cmap='hot')
    axarr[1,0].set_title('Wind [u] Map')
    plt.colorbar(im1, ax=axarr[1,0])

    im2 = axar[1,1].imshow(array3, cmap='hot')
    axar[1,1].set_title('Wind [v] Map')
    plt.colorbar(im2, ax=axarr[1,1])


    plt.pause(0.00001)

def loadHeatmap(axar, array1, array2, array3, world):
    im0.set_array(array1)
    im0.set_clim([array1.min(), array1.max()])

    full_grad_u, full_grad_v = world.calcPressureGrad(array1)

    im3.set_array(full_grad_u)
    im3.set_clim([full_grad_u.min(), full_grad_u.max()])

    im4.set_array(full_grad_v)
    im4.set_clim([full_grad_v.min(), full_grad_v.max()])

    im1.set_array(array2)
    im1.set_clim([array2.min(), array2.max()])

    im2.set_array(array3)
    im2.set_clim([array3.min(), array3.max()])

    plt.pause(0.00001)

if __name__ == "__main__":
    logger = Logger(log_ID="ui")

    wld = World(world_name="world", wld_grid_size=100)
    sim = Control(wld)

    wld.clear_data()

    logger.log("World and Controller ready")

    plt.ion()
    fig, axarr = plt.subplots(2,3)

    logger.log("Pyplot ready, beggining sim")

    # Add test sources
    added_p_grid = np.zeros((wld.grid_size, wld.grid_size))
    added_p_grid[20,50] = -15.
    added_p_grid[20-1,50] = -15.
    added_p_grid[20+1,50] = -15.
    added_p_grid[20,50-1] = -15.
    added_p_grid[20,50+1] = -15.

    added_p_grid[50,70] = 15.
    added_p_grid[50-1,70] = 15.
    added_p_grid[50+1,70] = 15.
    added_p_grid[50,70-1] = 15.
    added_p_grid[50,70+1] = 15.

    added_u_grid = np.zeros((wld.grid_size, wld.grid_size))
    added_u_grid[1:wld.grid_size-1, 1:wld.grid_size-1] = .0001

    added_v_grid = np.zeros((wld.grid_size, wld.grid_size))
    added_v_grid[1:wld.grid_size-1, 1:wld.grid_size-1] = .0001

    solver.add_source(wld.wld_grid_size, wld.air_pressure, added_p_grid, wld.dt)
    solver.add_source(wld.wld_grid_size, wld.air_vel_u, added_u_grid, wld.dt)
    solver.add_source(wld.wld_grid_size, wld.air_vel_v, added_v_grid, wld.dt)

    # Start ui
    startHeatmap(axarr, wld.air_pressure, wld.air_vel_u, wld.air_vel_v, wld)

    # Run simulation
    sim.running = True

    while not keyboard.is_pressed('x'):
        try:
            sim.tick()
        except Exception as e:
            logger.log("Error during tick {}: [{}]".format(sim.tickNum, e))
            break

        if keyboard.is_pressed('s'):
            loadHeatmap(axarr, wld.air_pressure, wld.air_vel_u, wld.air_vel_v, wld)
            logger.log("Showing data for tick {}".format(sim.tickNum))

        elif sim.tickNum % 100 == 0:
            logger.log("Reached tick {}".format(sim.tickNum))

        ## Output average difference between current and previous pressure maps to check the data isnt blowing up
        # if sim.tickNum % 5 == 0:
        #     avgNew = 0
        #     avgOld = 0
        #     avgNew += np.sum(wld.air_pressure) / wld.grid_size ** 2
        #     avgOld += np.sum(wld.air_pressure_prev) / wld.grid_size ** 2
        #     dif = avgNew - avgOld
        #
        #     print("Reached tick {}\navg dif is {}".format(sim.tickNum, dif))

    sim.running = False
