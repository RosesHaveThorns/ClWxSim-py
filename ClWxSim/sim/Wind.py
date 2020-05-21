"""Contains functions for wind map calculations"""

import ClWxSim.sim.fluid_solver as solver

import numpy as np
import math

PGF_modifier = 0.01
coriolis_modifier = 100

def tick(N, u, v, u0, v0, visc, dt, x_grad_u, x_grad_v, x_grad_u_prev, x_grad_v_prev, w, apply_pgf=True, remove_pgf=True):
    """Calculates the advection, diffusion, coriolis effect and pressure gradient force affects on the wind velocity arrays over a single tick

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
        x_grad_v_prev (array of size N+2): The previous value of x_grad_u
        x_grad_u_prev (array of size N+2): The previous value of x_grad_v
        w (float): Planet's angular velocity
        apply_pgf (bool, optional): If false, will not add new Pressure Gradient Force (only false until pressure has smoothed)
        remove_pgf (bool, optional) If false, will not remove old Pressure Gradient Force (only false for first tick PGF is applied)
    """
    #  Pressure Gradient Force: Remove old gradient, apply new gradient
    if remove_pgf:
        u[0:N+2, 0:N+2] -= x_grad_u_prev[0:N+2, 0:N+2] * PGF_modifier * dt
        v[0:N+2, 0:N+2] -= x_grad_v_prev[0:N+2, 0:N+2] * PGF_modifier * dt
    if apply_pgf:
        u[0:N+2, 0:N+2] += x_grad_u[0:N+2, 0:N+2] * PGF_modifier * dt
        v[0:N+2, 0:N+2] += x_grad_v[0:N+2, 0:N+2] * PGF_modifier * dt

    # Coriolis Effect: Caused by planet's rotation
    for i in range(N+2):
        for j in range(N+2):
            v[i, j] += 2 * w * np.sin(calcLat(N, i)) * dt * coriolis_modifier# * u[i, j]

    # Advection and Diffusion: As per the paper "Real-Time Fluid Dynamics for Games" by Jos Stam

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

def calcLat(N, y):
    """returns the latitude (in rad) of a given y axis value, assumes map's latittude is linear"""
    lat = ((N - y) / N * 2 * math.pi) - math.pi
    return lat
