import os


class Reporter():
    """This class is used to report data to disk.

    Args:

        model: The PETAL model.
    """

    def __init__(self, config):
        self.time = []
        self.nectar = []
        self.pollen = []


        self.folder_out = config['folder_out']
        if not os.path.isdir(self.folder_out):
            os.makedirs(self.folder_out)

        self.data_out = config["out_file"]

        # for module_name, config in config.items()
