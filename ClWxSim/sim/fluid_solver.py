"""Contains functions for calculating 2D weather effects, including advection, diffuse and the coriolis effect"""

import math
import numpy as np

def add_source(N, x, s, dt):
    """Adds s to x, taking into account dt

    Args:
        N (int): Size of arrays excluding boundary cells
        x (array of size N+2): Main array
        s (array of size N+2): Secondary array to be added to x
        dt (float): Length of time of each tick
    """
    size = (N + 2)
    x[0:size, 0:size] += dt * s[0:size, 0:size]

def set_bnd(N, b, x):
    """Sets boundary cell values to their adjacent central cell

    Args:
        N (int): Size of array excluding boundary cells
        b (int): Defines whether to make the boundary values negative (0 = none, 1 = only left and right, 2 = only top and bottom)
        x (array of size N+2): The array to set the boundary cell values of
    """
    # Sets boundary wall cell values to the adjacent central cell
    # If b=1 Left and Right walls are negative (cancels out adjacent central cell velocity?)
    # If b=2 Top and Bottom walls are negative (cancels out adjacent central cell velocity?)
    for i in range(1, N + 1):
        if b == 1:
            x[0, i] = -x[1, i]      # Left wall
            x[N + 1, i] = -x[N, i]  # Right wall
        else:
            x[0, i] = x[1, i]       # Left wall
            x[N + 1, i] = x[N, i]   # Right wall

        if b == 2:
            x[i, 0] = -x[i, 1]      # Bottom wall
            x[i, N + 1] = -x[i, N]  # Top wall
        else:
            x[i, 0] = x[i, 1]       # Bottom wall
            x[i, N + 1] = x[i, N]   # Top wall

    # Average corners from adjacent boundary cells
    x[0, 0] = 0.5 * (x[1, 0] + x[0, 1])
    x[0, N + 1] = 0.5 * (x[1, N + 1] + x[0, N])
    x[N + 1, 0] = 0.5 * (x[N, 0] + x[N + 1, 1])
    x[N + 1, N + 1] = 0.5 * (x[N, N + 1] + x[N + 1, N])

def lin_solve(N, b, x, x0, a, c):
    """Gauss-Seidel linear equation solver

    Args:
        N (int): Size of array excluding boundary cells
        b (int): Defines whether to make the boundary values negative (0 = none, 1 = only left and right, 2 = only top and bottom)
        x (array of size N+2): The array to solve for
        x0 (array of size N+2): The previous value of x
        a (float): Linear solver parameter
        c (float): Linear solver parameter
    """

    for k in range(0, 20):
        x[1:N + 1, 1:N + 1] = (x0[1:N + 1, 1:N + 1] + a *
                               (x[0:N, 1:N + 1] +
                                x[2:N + 2, 1:N + 1] +
                                x[1:N + 1, 0:N] +
                                x[1:N + 1, 2:N + 2])) / c
        set_bnd(N, b, x)

def diffuse(N, b, x, x0, diff, dt):
    """Calculates the changes to array x after diffusion

    Args:
        N (int): Size of array excluding boundary cells
        b (int): Defines whether to make the boundary values negative (0 = none, 1 = only left and right, 2 = only top and bottom)
        x (array of size N+2): The array to diffuse
        x0 (array of size N+2): The previous value of x
        diff (float > 0): Rate of diffusion
        dt (float): Length of time of each tick
    """

    a = dt * diff * N * N
    lin_solve(N, b, x, x0, a, 1 + 4 * a)

def advect(N, b, d, d0, u, v, dt):
    """Calculates the changes to array d after advection due to the vector arrays [u v]

    Args:
        N (int): Size of array excluding boundary cells
        b (int): Defines whether to make the boundary values negative (0 = none, 1 = only left and right, 2 = only top and bottom)
        d (array of size N+2): The density array, which will be advected by [u v]
        d0 (array of size N+2): The previous value of d
        u (array of size N+2): The x component velocity vector array
        v (array of size N+2): The y component velocity vector array
        dt (float): Length of time of each tick
    """

    dt0 = dt * N
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            x = i - dt0 * u[i, j]
            y = j - dt0 * v[i, j]
            if x < 0.5:
                x = 0.5
            if x > N + 0.5:
                x = N + 0.5
            i0 = int(x)
            i1 = i0 + 1
            if y < 0.5:
                y = 0.5
            if y > N + 0.5:
                y = N + 0.5
            j0 = int(y)
            j1 = j0 + 1

            s1 = x - i0
            s0 = 1 - s1
            t1 = y - j0
            t0 = 1 - t1

            d[i, j] = (s0 * (t0 * d0[i0, j0] + t1 * d0[i0, j1]) + s1 * (t0 * d0[i1, j0] + t1 * d0[i1, j1]))
    set_bnd(N, b, d)


def project(N, u, v, p, div):
    """project."""

    h = 1.0 / N
    div[1:N + 1, 1:N + 1] = (-0.5 * h *
                             (u[2:N + 2, 1:N + 1] - u[0:N, 1:N + 1] +
                              v[1:N + 1, 2:N + 2] - v[1:N + 1, 0:N]))
    p[1:N + 1, 1:N + 1] = 0
    set_bnd(N, 0, div)
    set_bnd(N, 0, p)
    lin_solve(N, 0, p, div, 1, 4)
    u[1:N + 1, 1:N + 1] -= 0.5 * (p[2:N + 2, 1:N + 1] - p[0:N, 1:N + 1]) / h
    v[1:N + 1, 1:N + 1] -= 0.5 * (p[1:N + 1, 2:N + 2] - p[1:N + 1, 0:N]) / h
    set_bnd(N, 1, u)
    set_bnd(N, 2, v)

def coriolis(N, u, v, dt, w, mod, wld):
    """calclates wind acceleration due to the coriolis effect"""
    u_add = np.zeros((N+2, N+2))
    v_add = np.zeros((N+2, N+2))

    for i in range(N+1):
        for j in range(N+1):
            u_add[i,j] = v[i, j] * 2 * w * math.sin(math.radians(calc_lat(N, i))) * mod
            v_add[i,j] = -u[i, j] * 2 * w * math.sin(math.radians(calc_lat(N, i))) * mod

    wld.dbg_coriolis_u[0:N+2,0:N+2] = u_add[0:N+2,0:N+2]
    wld.dbg_coriolis_v[0:N+2,0:N+2] = v_add[0:N+2,0:N+2]

    add_source(N, u, u_add, dt)
    add_source(N, v, v_add, dt)

    set_bnd(N, 1, u)
    set_bnd(N, 2, v)

def calc_lat(N, y):
    """returns the latitude (in deg) of a given y axis value, assumes map's latittude is linear and y=0 is the south pole"""
    lat = -(((N - y) / N * 180) - 90)
    return lat
