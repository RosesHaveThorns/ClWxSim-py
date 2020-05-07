"""Contains functions for wind map calculations"""

import ClWxSim.sim.fluid_solver as solver

def tick(N, u, v, u0, v0, visc, dt):
    """Calculates the advection and diffusion of the pressure wind velocity arrays over a single tick

    Args:
        N (int): Size of array excluding boundary cells
        u (array of size N+2): The x component velocity vector array
        v (array of size N+2): The y component velocity vector array
        u0 (array of size N+2): The previous value of u
        v0 (array of size N+2): The previous value of v
        visc (float > 0): Rate of diffusion of vectors
        dt (float): Length of time of each tick
    """

    solver.add_source(N, u, u0, dt)
    solver.add_source(N, v, v0, dt)
    u0, u = u, u0  # swap
    solver.diffuse(N, 1, u, u0, visc, dt)
    v0, v = v, v0  # swap
    solver.diffuse(N, 2, v, v0, visc, dt)
    solver.project(N, u, v, u0, v0)
    u0, u = u, u0  # swap
    v0, v = v, v0  # swap
    solver.advect(N, 1, u, u0, u0, v0, dt)
    solver.advect(N, 2, v, v0, u0, v0, dt)
    solver.project(N, u, v, u0, v0)
