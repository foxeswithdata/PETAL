import copy
from curses import initscr

import pandas as pd

from petal.simple_plant import defaultSimplePlant
from petal.simple_plant import SimplePlant

class PlantRunner:

    def __init__(self, config):
        self.plants = []

        # Read in default traits
        default_simple_plant = defaultSimplePlant()
        self.initSimplePlant(config['plant']['simple_trait_file'], default_simple_plant)

    def initSimplePlant(self, simple_plant_traits, default_simple_plant):
        # read file
        default_plant = default_simple_plant

        colony_plants_df =  pd.read_csv(simple_plant_traits)
        for index, row in colony_plants_df.iterrows():
            plant = copy.deepcopy(default_plant)
            plant.name = row['species_name'] if pd.notna(row['species_name']) else default_plant.name
            self.plants.append(plant)

    def calculateRates(self, temperature):
        print("calculating rates")

        nectar_rates = 0
        pollen_rates = 0

        for plant in self.plants:
            plant.nectarProductionRate(temperature)
            plant.pollenProductionRate(temperature)
            plant.growthRate()
            plant.mortalityRate()
            nectar_rates += plant.dNdt
            pollen_rates += plant.dPdt

        return[nectar_rates, pollen_rates]

    def step(self, solver):
        print("stepping")

        for plant in self.plants:
            plant.step(solver)

    def print(self):
        # iterate through plants to print them
        for plant in self.plants:
            plant.print()