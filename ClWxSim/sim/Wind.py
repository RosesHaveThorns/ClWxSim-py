"""Contains functions for wind map calculations"""

import ClWxSim.sim.fluid_solver as solver

PGF_modifier = 0.1

def tick(N, u, v, u0, v0, visc, dt, x_grad_u, x_grad_v, x_grad_u_prev, x_grad_v_prev):
    """Calculates the advection and diffusion of the pressure wind velocity arrays over a single tick

    Args:
        N (int): Size of array excluding boundary cells
        u (array of size N+2): The x component velocity vector array
        v (array of size N+2): The y component velocity vector array
        u0 (array of size N+2): The previous value of u
        v0 (array of size N+2): The previous value of v
        visc (float > 0): Rate of diffusion of vectors
        dt (float): Length of time of each tick
        x_grad_u (array of size N+2): The x component pressure gradient array
        x_grad_v (array of size N+2): The y component pressure gradient array
    """
    u[1:N+1, 1:N+1] -= x_grad_u_prev[1:N+1, 1:N+1] * PGF_modifier * dt
    v[1:N+1, 1:N+1] -= x_grad_v_prev[1:N+1, 1:N+1] * PGF_modifier * dt

    u[1:N+1, 1:N+1] += x_grad_u[1:N+1, 1:N+1] * PGF_modifier * dt
    v[1:N+1, 1:N+1] += x_grad_v[1:N+1, 1:N+1] * PGF_modifier * dt

    u0, u = u, u0  # swap
    v0, v = v, v0  # swap

    solver.diffuse(N, 1, u, u0, visc, dt)
    solver.diffuse(N, 2, v, v0, visc, dt)

    solver.project(N, u, v, u0, v0)

    u0, u = u, u0  # swap
    v0, v = v, v0  # swap

    solver.advect(N, 1, u, u0, u0, v0, dt)
    solver.advect(N, 2, v, v0, u0, v0, dt)

    solver.project(N, u, v, u0, v0)


    # TAKE AWAY OLD GRADIENT, ADD NEW GRADIENT, CALC ADVECTION AND DIFFUSION, representation
    # that way im not adding more stuff all the time, it wont explode

    # I think it will anyway? the pressure will just spread out super quick
    # Maybe remove the grad when advecting the pressure so pressure doesnt affect itself, but keep it in for humitity etc
