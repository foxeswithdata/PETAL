import pandas as pd

from petal.pollinator_runner import PollinatorRunner


class PatchRunner:

    def __init__(self, config):
        # initialise pollinators from config file
        self.pollinator = PollinatorRunner(config)
        self.plant = []

        self.pollinator.print()
