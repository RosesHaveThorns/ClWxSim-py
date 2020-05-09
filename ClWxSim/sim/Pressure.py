"""Contains functions for pressure map calculations"""

import ClWxSim.sim.fluid_solver as solver

def tick(N, x, x0, u, v, diff, dt):
    """Calculates the advection and diffusion of the pressure array over a single tick

    Args:
        N (int): Size of array excluding boundary cells
        x (array of size N+2): The density array, which will be advected by [u v]
        x0 (array of size N+2): The previous value of d
        u (array of size N+2): The x component velocity vector array
        v (array of size N+2): The y component velocity vector array
        diff (float > 0): Rate of diffusion
        dt (float): Length of time of each tick
    """

    x0, x = x, x0  # swap
    solver.diffuse(N, 0, x, x0, diff, dt)
    x0, x = x, x0  # swap
    solver.advect(N, 0, x, x0, u, v, dt)
