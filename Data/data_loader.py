class Loader:
    """Presents a number of functions for manipuating of the main data file."""

    def __init__(self, loc="weather_data.txt"):
        """Sets up a loader for a single main data file.

        Args:
            loc (str, optional): Location of main data file, defalts to 'weather_data.txt'
        """
        self.data_loc = loc

    def create(self, empty = True):
        pass

    def load(self):
        pass

    def store(self):
        pass

    def clear(self):
        pass
