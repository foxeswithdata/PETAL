import copy
import pandas as pd


class PlantRunner:

    def __init__(self, config):
        self.plant = []

        # Read in default traits