import pandas as pd
import

from petal.pollinator_runner import PollinatorRunner
from petal.plant_runner import PlantRunner

class PatchRunner:

    def __init__(self, config):
        # initialise pollinators from config file
        self.pollinator = PollinatorRunner(config)
        self.plant = PlantRunner(config)

        self.pollinator.print()
