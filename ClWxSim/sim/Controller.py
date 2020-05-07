from ClWxSim.utils.logging import Logger
import numpy as np

import ClWxSim.sim.pressure as p
import ClWxSim.sim.wind as w
import ClWxSim.sim.fluid_solver as solver

class Controller:
    """Sets up and runs weather simulations on a specified World object"""

    self.running = True

    def __init__(self, world):
        """Instatiaties a Controller object

        Args:
            world (World object): The world used to simulate weather
        """

        self.world = world
        self.logger = Logger(log_name="sim_controller")

    def start(self):
        logger.log("Starting Simulation")

        tick = 0
        while self.running:
            tick += 1

            w.tick(self.world.wld_grid_size, self.world.air_vel_u, self.world.air_vel_v, self.world.air_vel_u_prev, self.world.air_vel_v_prev, self.world.visc, self.world.dt)
            p.tick(self.world.wld_grid_size,  self.world.air_pressure,  self.world.air_pressure_prev, self.world.air_vel_u, self.world.air_vel_v,  self.world.diff,  self.world.dt)

            try:
                self.world.air_vel_u.round(decimals=5)
                self.world.air_vel_v.round(decimals=5)
                self.world.air_vel_u_prev.round(decimals=5)
                self.world.air_vel_v_prev.round(decimals=5)
                self.world.air_pressure.round(decimals=5)
                self.world.air_pressure_prev.round(decimals=5)
            except Exception as e:
                self.logger.log("Error rounding arrays during tick {}: [{}]".format(tick, e))
