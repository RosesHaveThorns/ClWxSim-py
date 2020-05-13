from ClWxSim.utils.logging import Logger
import numpy as np

import ClWxSim.sim.pressure as p
import ClWxSim.sim.wind as w
import ClWxSim.sim.fluid_solver as solver

class Controller:
    """Sets up and runs weather simulations on a specified World object"""

    running = False
    tickNum = 0

    def __init__(self, world):
        """Instatiaties a Controller object

        Args:
            world (World object): The world used to simulate weather
        """

        self.world = world
        self.logger = Logger(log_ID="sim_controller")


    def tick(self):
        if self.running:
            self.tickNum += 1

            pressure_grad_u, pressure_grad_v = self.world.calcPressureGrad(self.world.air_pressure)

            w.tick(self.world.wld_grid_size, self.world.air_vel_u, self.world.air_vel_v, self.world.air_vel_u_prev, self.world.air_vel_v_prev, self.world.visc, self.world.dt, pressure_grad_u, pressure_grad_v, self.world.air_pressure_grad_u_prev, self.world.air_pressure_grad_v_prev)
            p.tick(self.world.wld_grid_size,  self.world.air_pressure,  self.world.air_pressure_prev, self.world.air_vel_u, self.world.air_vel_v,  self.world.diff,  self.world.dt)

            self.world.air_pressure_grad_u_prev, self.world.air_pressure_grad_v_prev = pressure_grad_u, pressure_grad_v

            try:
                self.world.air_vel_u = self.world.air_vel_u.round(decimals=10)
                self.world.air_vel_v = self.world.air_vel_v.round(decimals=10)
                self.world.air_vel_u_prev = self.world.air_vel_u_prev.round(decimals=10)
                self.world.air_vel_v_prev = self.world.air_vel_v_prev.round(decimals=10)
                self.world.air_pressure = self.world.air_pressure.round(decimals=10)
                self.world.air_pressure_prev = self.world.air_pressure_prev.round(decimals=10)
            except Exception as e:
                self.logger.log("ERROR while rounding arrays during tick {}: [{}]".format(self.tickNum, e))
        else:
            self.logger.log("WARNING: Controller is not running, have you set Controller.running to True?")
