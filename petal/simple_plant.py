import math
from petal.plant import PlantBase

class SimplePlant(PlantBase):

    def __init__(self, name, growthRate, nectarProductionRate, pollenProductionRate):
        self.name = name

        ## state variables
        self.density = 1  # gC/m2  ## equivalent to structural biomass - need to determine how this is handled

        # rates
        self.dGdt = 1  ## Growth rate
        self.dMdt = 1  ## mortality rate
        self.dNdt = 1  ## Nectar production rate
        self.dPdt = 1  ## Pollen production rate

    def initDensity(self):
        pass

    def mortalityRate(self):
        pass

    def growthRate(self):
        pass

    def nectarProductionRate(self, temperature):
        return(self.dNdt) ## Nectar production rate

    def pollenProductionRate(self, temperature):
        return(self.dPdt) ## Pollen production rate

    def print(self):
        print(f"Plant Name: {self.name}")
        print(f"Density: {self.density}")
        print(f"Growth Rate: {self.dGdt}")
        print(f"Mortality Rate: {self.dMdt}")
        print(f"Nectar Production Rate: {self.dNdt}")
        print(f"Pollen Production Rate: {self.dPdt}")

    def step(self, solver):
        pass

def defaultSimplePlant():
    # Define default traits for a simple plant
    return SimplePlant(name="DefaultPlant", growthRate=1.0, nectarProductionRate=0.5, pollenProductionRate=0.5)