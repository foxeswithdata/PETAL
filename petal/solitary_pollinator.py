from petal.pollinator import PollinatorBase


class SolitaryPollinator(PollinatorBase):

    def __init__(self, name):
        self.name = name
        self.density = 1
        self.dGdt = 1
        self.dMdt = 1
        self.dBdt = 1
        print("Hello World")

    def initDensity(self):
        print("Hello World")

    def mortalityRate(self):
        print("Hello World")

    def growthRate(self):
        print("Hello World")

    def birthRate(self):
        print("Hello World")

    def nectarHarvestPotentialRate(self):
        print("Hello World")

    def pollenHarvestPotentialRate(self):
        print("Hello World")
    def print(self):
        print("Solitary Pollinator")
        print(self.name)
