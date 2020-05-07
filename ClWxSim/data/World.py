from ClWxSim.utils.logging import Logger
import numpy as np

class World:
    """A representation of a planet's terrain, climate and weather

    Attributes:
        air_humidity (float array): Size defined by grid_size
        air_vel_u (tuple array): Array storing x vectors representing the wind velocity in each grid square, Size defined by grid_size
        air_vel_v (tuple array): Array storing v vectors representing the wind velocity in each grid square, Size defined by grid_size
        air_temp (float array): Size defined by grid_size
        air_pressure (float array): Array storing the air pressure at sea level in each grid square, measured in mbar, size defined by grid_size
        old_air_pressure (float array): Array storing a copy of air_pressure as it was before the last tick
        air_precip (float array): Size defined by grid_size
        ground_temp (float array): Size defined by grid_size
        ground_height (float array): Size defined by grid_size
        ground_water (float array): Size defined by grid_size
        grid_size (tuple): Height and Width of all 2D world data arrays
        grid_sq_size (int): Height and Width of each grid square, measured in km
        world_name (str): The name of the world
        atmos_height (float): Height of the World's atmosphere assuming a uniform density, measured in km
        grid_sq_vol (float): An esimation of the volume of air a grid square holds, measured in km^3
    """

    # -- Attributes --
    dt = .5         # Length of time for each tick
    diff = 0.00001  # Pressure diffusion rate
    visc = 0.00001  # Wind diffusion rate

    # -- Functions --

    def __init__(self, world_name, data_loc="", wld_grid_size=72, grid_sq_size=100, atmos_height=8.5, starting_pressure=1013.25):
        """Creates a new World object

        Args:
            wld_grid_size (int, optional): Height and Width excluding boundary cells of all 2D world data arrays to be created, defaults to 72
            world_name (str): The name to give the World
            loc (str, optional): Folder to store this World object's data, defaults to this script's directory ("")
            starting_pressure (float, optional): Initial air pressure (in mbar) for all grid squares, defaults to 1013.25 mbar
            grid_sq_size (int, optional): Height and Width of each grid square (in km), defaults to 100 km
            atmos_height (float, optional): Height of the World's atmosphere assuming a uniform density, defaults to 8.5 km
        """

        # Set attrs
        self.world_name = world_name
        # self.data_loc = data_loc

        self.starting_pressure = starting_pressure

        self.wld_grid_size = wld_grid_size
        self.grid_size = wld_grid_size + 2
        # self.grid_sq_size = grid_sq_size
        # self.atmos_height = atmos_height

        # self.grid_sq_vol = atmos_height * (grid_sq_size ** 2)

        # Create world data arrays
        self.air_vel_u = np.zeros((self.grid_size, self.grid_size))    # x wind velocity map
        self.air_vel_u_prev = np.zeros((self.grid_size, self.grid_size))

        self.air_vel_v = np.zeros((self.grid_size, self.grid_size))    # y wind velocity map
        self.air_vel_v_prev = np.zeros((self.grid_size, self.grid_size))

        self.air_pressure = np.full((self.grid_size, self.grid_size), starting_pressure)  # pressure map
        self.air_pressure_prev = np.full((self.grid_size, self.grid_size), starting_pressure)

        # self.air_humidity = np.zeros((grid_size, grid_size))
        #
        # self.air_temp = np.zeros((grid_size, grid_size))
        #
        # self.air_precip = np.zeros((grid_size, grid_size))
        #
        # self.ground_temp = np.zeros((grid_size, grid_size))
        #
        # self.ground_height = np.zeros((grid_size, grid_size))
        #
        # self.ground_water = np.zeros((grid_size, grid_size))

        # Setup Logger
        self.logger = Logger(log_ID="world-{}".format(self.world_name))

        self.logger.log("{} instantiated".format(self.world_name))

    def clear_data(self):
        """clear all weather data"""

        self.air_vel_u[0:self.grid_size, 0:self.grid_size] = 0.0
        self.air_vel_v[0:self.grid_size, 0:self.grid_size] = 0.0

        self.air_vel_u_prev[0:self.grid_size, 0:self.grid_size] = 0.0
        self.air_vel_v_prev[0:self.grid_size, 0:self.grid_size] = 0.0

        self.air_pressure[0:self.grid_size, 0:self.grid_size] = self.starting_pressure
        self.air_pressure_prev[0:self.grid_size, 0:self.grid_size] = self.starting_pressure

    # def load(self):
    #     try:
    #         np.load(data_loc+"air_humidity.cws")
    #         np.load(data_loc+"air_vectors.cws")
    #         np.load(data_loc+"air_temp.cws")
    #         np.load(data_loc+"air_pressure.cws")
    #         np.load(data_loc+"air_precip.cws")
    #
    #         np.load(data_loc+"ground_temp.cws")
    #         np.load(data_loc+"ground_height.cws")
    #         np.load(data_loc+"ground_water.cws")
    #
    #         self.logger.log("{} loaded".format(world_name))
    #     except Exception as e:
    #         self.logger.log("{} failed loading: [{e}]".format(world_name, e))
    #
    # def save(self):
    #     try:
    #         np.save(data_loc+"air_humidity.cws", self.air_humidity)
    #         np.save(data_loc+"air_vectors.cws", self.air_vectors)
    #         np.save(data_loc+"air_temp.cws", self.air_temp)
    #         np.save(data_loc+"air_pressure.cws", self.air_pressure)
    #         np.save(data_loc+"air_precip.cws", self.air_precip)
    #
    #         np.save(data_loc+"ground_temp.cws", self.ground_temp)
    #         np.save(data_loc+"ground_height.cws", self.ground_height)
    #         np.save(data_loc+"ground_water.cws", self.ground_water)
    #
    #         self.logger.log("{} saved".format(world_name))
    #     except Exception as e:
    #         self.logger.log("{} failed saving: [{}]".format(world_name, e))
