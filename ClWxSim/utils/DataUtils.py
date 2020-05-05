from ClWxSim.utils.logging import Logger

class DataUtils:
    """A collection of utility functions for handling data and variables"""

    def __init__(self):
        self.logger = Logger()

    def swap(self, arg1, arg2):
        tmp = arg1
        arg1 = arg2
        arg2 = tmp

        return arg1, arg2
