from ClWxSim.utils.logging import Logger
import numpy as np

class Controller:
    """Sets up and runs weather simulations on a specified World object"""

    def __init__(self, world):
        """Instatiaties a Controller object

        Args:
            world (World object): The world used to simulate weather
        """

        self.world = world

    def start(self):
        pass
