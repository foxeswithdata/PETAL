import copy
import pandas as pd
from petal.colony_pollinator import ColonyPollinator
from petal.solitary_pollinator import SolitaryPollinator


class PollinatorRunner:

    def __init__(self, config):

        self.pollinator = []

        # Read in default traits
        default_colony_poll = ColonyPollinator(name = "default")
        default_solitary_poll = SolitaryPollinator(name="default")

        self.initColonyPollinators(config['pollinator']['colony_trait_file'], default_colony_poll)
        self.initSolitaryPollinators(config['pollinator']['solitary_trait_file'], default_solitary_poll)

    def initColonyPollinators(self, colony_pollinator_traits, default_colony_poll):
        # read file
        default_poll = default_colony_poll

        colony_pollinators_df =  pd.read_csv(colony_pollinator_traits)
        for index, row in colony_pollinators_df.iterrows():
            pollinator = copy.deepcopy(default_poll)
            pollinator.name = row['species_name'] if row['species_name'] is not None else default_poll.name
            self.pollinator.append(pollinator)


    def initSolitaryPollinators(self, solitary_pollinator_traits, default_solitary_poll):
        # read file
        solitary_pollinators_df = pd.read_csv(solitary_pollinator_traits)
        for index, row in solitary_pollinators_df.iterrows():
            pollinator = copy.deepcopy(default_solitary_poll)
            pollinator.name = row['species_name'] if row['species_name'] is not None else default_solitary_poll.name
            self.pollinator.append(pollinator)

    def calculateRates(self, environment, availableNectarReserves, availablePollenReserves):

        ## Determine nectar+pollen collection
        nectarHarvestPotential = []
        pollenHarvestPotential = []
        for index, pollinator in self.pollinator:
            ## To do calculate effort for each pollinator
            nectarHarvestPotential.append(pollinator.nectarHarvestPotentialRate(environment))
            pollenHarvestPotential.append(pollinator.pollenHarvestPotentialRate(environment))

        totalNectarHarvestPotential = sum(nectarHarvestPotential)
        nectarHarvestPotentialPortion = nectarHarvestPotential / totalNectarHarvestPotential


        if totalNectarHarvestPotential > availableNectarReserves:

            ## here the maximum available nectar is used
            for index, pollinator in self.pollinator:
                actualHarvestRate = nectarHarvestPotentialPortion[index] * availableNectarReserves
                pollinator.nectarHarvest(actualHarvestRate)

            else:
                actualHarvestRate = nectarHarvestPotential[index]
                pollinator.nectarHarvest(actualHarvestRate)

        totalPollenHarvestPotential = sum(pollenHarvestPotential)
        pollenHarvestPotentialPortion = pollenHarvestPotential / totalPollenHarvestPotential

        if totalPollenHarvestPotential > availablePollenReserves:
            ## here the maximum available nectar is used
            for index, pollinator in self.pollinator:
                actualHarvestRate = pollenHarvestPotentialPortion[index] * availablePollenReserves
                pollinator.nectarHarvest(actualHarvestRate)
        else:
            for index, pollinator in self.pollinator:
                actualHarvest = nectarHarvestPotential[index]
                pollinator.nectarHarvest(actualHarvest)

        ## calculate growth rates


    def step(self, solver):
        # Todo: complete
        for pollinator in self.pollinator:
            pollinator.step(solver)


    def print(self):
        for pollinator in self.pollinator:
            print(pollinator.print())



