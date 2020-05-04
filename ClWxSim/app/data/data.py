from ClWxSim.app.utils.logging import Logger
import numpy as np

class World:
    """A representation of a planet's terrain, climate and weather

    Attributes:
        air_humidity (float array): Size defined by grid_size
        air_vectors (float array): Size defined by grid_size
        air_temp (float array): Size defined by grid_size
        air_pressure (float array): Size defined by grid_size
        air_precip (float array): Size defined by grid_size
        ground_temp (float array): Size defined by grid_size
        ground_height (float array): Size defined by grid_size
        ground_water (float array): Size defined by grid_size
        grid_size (tuple): Size of all world data arrays
        world_name (str): The name of the world
    """

    # -- ATTRIBUTES --

    grid_size = (72,72)
    world_name = ""

    data_loc = ""

    # -- Functions --

    def __init__(self, grid_size, world_name, loc=""):
        """Creates a new World object

        Args:
            grid_size (tuple): Size of all world data arrays to be created
            world_name (str): The name to give the World
            loc (str): Folder to store this World object's data, defaults to this script's directory
        """
        # Setup Logger
        self.logger = Logger()

        # Set attrs
        self.world_name = world_name
        self.grid_size = grid_size
        self.data_loc = loc

        # Create world data arrays
        self.air_humidity = np.zeros(grid_size)
        self.air_vectors = np.zeros(grid_size)
        self.air_temp = np.zeros(grid_size)
        self.air_pressure = np.zeros(grid_size)
        self.air_precip = np.zeros(grid_size)

        self.ground_temp = np.zeros(grid_size)
        self.ground_height = np.zeros(grid_size)
        self.ground_water = np.zeros(grid_size)

        self.logger.log("{world_name} instantiated".format(world_name))

    def load(self):
        try:
            np.load(data_loc+"air_humidity.cws")
            np.load(data_loc+"air_vectors.cws")
            np.load(data_loc+"air_temp.cws")
            np.load(data_loc+"air_pressure.cws")
            np.load(data_loc+"air_precip.cws")

            np.load(data_loc+"ground_temp.cws")
            np.load(data_loc+"ground_height.cws")
            np.load(data_loc+"ground_water.cws")

            self.logger.log("{world_name} loaded".format(world_name))
        except Exception as e:
            self.logger.log("{world_name} failed loading: [{e}]".format(world_name, e))

    def save(self):
        try:
            np.save(data_loc+"air_humidity.cws", self.air_humidity)
            np.save(data_loc+"air_vectors.cws", self.air_vectors)
            np.save(data_loc+"air_temp.cws", self.air_temp)
            np.save(data_loc+"air_pressure.cws", self.air_pressure)
            np.save(data_loc+"air_precip.cws", self.air_precip)

            np.save(data_loc+"ground_temp.cws", self.ground_temp)
            np.save(data_loc+"ground_height.cws", self.ground_height)
            np.save(data_loc+"ground_water.cws", self.ground_water)

            self.logger.log("{world_name} saved".format(world_name))
        except Exception as e:
            self.logger.log("{world_name} failed saving: [{e}]".format(world_name, e)) 
