import copy
import pandas as pd
from petal.colony_pollinator import ColonyPollinator
from petal.colony_pollinator import defaultColonyPollinator
from petal.solitary_pollinator import SolitaryPollinator
from petal.solitary_pollinator import defaultSolitaryPollinator


class PollinatorRunner:

    def __init__(self, config):

        self.pollinators = []
        self.migrationRates = []

        # Read in default traits
        default_colony_poll = defaultColonyPollinator()
        default_solitary_poll = defaultSolitaryPollinator()

        self.initColonyPollinators(config['pollinator']['colony_trait_file'], default_colony_poll)
        self.initSolitaryPollinators(config['pollinator']['solitary_trait_file'], default_solitary_poll)

    def initColonyPollinators(self, colony_pollinator_traits, default_colony_poll):
        # read file
        colony_pollinators_df =  pd.read_csv(colony_pollinator_traits)
        for index, row in colony_pollinators_df.iterrows():
            pollinator = copy.deepcopy(default_colony_poll)
            pollinator.name = row['species_name'] if pd.notna(row['species_name']) else default_colony_poll.name
            self.pollinators.append(pollinator)


    def initSolitaryPollinators(self, solitary_pollinator_traits, default_solitary_poll):
        # read file
        solitary_pollinators_df = pd.read_csv(solitary_pollinator_traits)
        for index, row in solitary_pollinators_df.iterrows():
            pollinator = copy.deepcopy(default_solitary_poll)
            pollinator.name = row['species_name'] if pd.notna(row['species_name']) else default_solitary_poll.name
            self.pollinators.append(pollinator)

    def calculateRates(self, environment, availableNectar, availablePollen, migrationRates):

        ## Determine nectar+pollen collection
        nectarHarvestPotential = []
        pollenHarvestPotential = []
        for pollinator in self.pollinators:
            ## To do calculate effort for each pollinator
            nectarHarvestPotential.append(pollinator.nectarHarvestPotentialRate(environment))
            pollenHarvestPotential.append(pollinator.pollenHarvestPotentialRate(environment))

        totalNectarHarvestPotential = sum(nectarHarvestPotential)
        nectarHarvestPotentialPortion = nectarHarvestPotential / totalNectarHarvestPotential

        if totalNectarHarvestPotential > availableNectar:

            ## here the maximum available nectar is used
            for index, pollinator in enumerate(self.pollinators):
                actualHarvestRate = nectarHarvestPotentialPortion[index] * availableNectar
                pollinator.nectarHarvest(actualHarvestRate)

            else:
                actualHarvestRate = nectarHarvestPotential[index]
                pollinator.nectarHarvest(actualHarvestRate)

        totalPollenHarvestPotential = sum(pollenHarvestPotential)
        pollenHarvestPotentialPortion = pollenHarvestPotential / totalPollenHarvestPotential

        if totalPollenHarvestPotential > availablePollen:
            ## here the maximum available nectar is used
            for index, pollinator in enumerate(self.pollinators):
                actualHarvestRate = pollenHarvestPotentialPortion[index] * availablePollen
                pollinator.nectarHarvest(actualHarvestRate)
        else:
            for index, pollinator in enumerate(self.pollinators):
                actualHarvest = nectarHarvestPotential[index]
                pollinator.nectarHarvest(actualHarvest)

        ## calculate rates
        for index, pollinator in enumerate(self.pollinators):
            pollinator.growthRate()
            pollinator.birthRate()
            pollinator.mortalityRate()

        return[min(totalNectarHarvestPotential, availableNectar),
               min(totalPollenHarvestPotential, availablePollen)]


    def step(self, solver):
        # Todo: complete
        for pollinator in self.pollinators:
            pollinator.step(solver)

    def print(self):
        for pollinator in self.pollinators:
            print(pollinator.print())



