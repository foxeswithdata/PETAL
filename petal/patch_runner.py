import pandas as pd

from petal.pollinator_runner import PollinatorRunner
from petal.plant_runner import PlantRunner

## Patch runner stores plants, pollinators and available pollen+nectar reserves

class PatchRunner:

    def __init__(self, config):
        # initialise pollinators from config file
        self.pollinator = PollinatorRunner(config)
        self.plant = PlantRunner(config)

        self.availableNectarReserves = []
        self.availablePollenReserves = []

        self.dNdt = 0
        self.dPdt = 0

        self.pollinator.print()
        self.plant.print()

    def calculateRates(self, environment, migrationRates = 0):
        [plantNectar, plantPollen] = self.plant.calculateRates(environment)
        [pollinatorNectar, pollinatorPollen] = self.pollinator.calculateRates(environment,
                                       self.availableNectarReserves,
                                       self.availablePollenReserves,
                                       migrationRates)

        self.dNdt = plantNectar + pollinatorNectar
        self.dPdt = plantPollen + plantPollen


    def step(self, solver):
        self.plant.step(solver)
        self.pollinator.step(solver)

        self.availableNectarReserves += self.dNdt
        self.availablePollenReserves += self.dPdt