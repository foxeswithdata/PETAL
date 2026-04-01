import math
from petal.pollinator import PollinatorBase

class ColonyPollinator(PollinatorBase):

    def __init__(self,
                 name,
                 foragingEffortNectar,
                 foragingEffortPollen,
                 foragingAllocationTrait):

        ## traits
        self.name = name
        self.foragingEffortNectar = foragingEffortNectar # Phi_N
        self.foragingEffortPollen = foragingEffortPollen # Phi_P
        self.foragingAllocationTrait = foragingAllocationTrait ## beta_F

        ## state variables
        self.density = 1 # gC/m2  ## equivalent to structural biomass - need to determine how this is handled

        self.reservesPollen = 0
        self.reservesNectar = 0

        self.reproduction = 0

        # rates
        self.dGdt = 1 ## Growth rate
        self.dMdt = 1 ## mortality rate
        self.dBdt = 1 ## Birth/Reproduction rate
        self.dRdt = 1 ## Respiration rate
        self.dMigdR = 1 ## Migration rate

        ## collection
        self.dPndt = 1 ## Nectar harvest rate
        self.dPpdt = 1 ## Pollen harvest rate

        ## egestion
        self.dEndt = 1 ## Egestion nectar rate
        self.dEpdt = 1 ## Egestion pollen rate

    def initDensity(self):
        ## todo: implement
        print("Hello World")

    def mortalityRate(self):
        mortality_natural = 1
        d_starv = 1
        s_n_tol = 1
        mortality_starvation = d_starv * math.exp(-self.reservesNectar / s_n_tol)
        ## todo: ignore for now
        mortality_pesticide = 0
        self.dMdt = (mortality_natural + mortality_starvation + mortality_pesticide) * self.density

    def birthRate(self):
        ## todo: implement
        print("Hello World")

    def heatingRate(self):
        ## todo: implement
        print("Hello World")

    def flightCost(self):
        ## todo: implement
        print("Hello World")

    def egestionNectarRate(self):
        ## todo: implement
        egestionNectar = 1
        self.dEndt = 1

    def egestionPollenRate(self):
        ## todo: implement
        egestionPollen = 1
        self.dEpdt = 1

    def respirationRate(self, temperature):
        somaticMaintenanceRespirationRate = 1
        foragingRespirationRate = 1
        ## Todo: divide foraging respiration into nectar and pollen
        self.dRdt = (somaticMaintenanceRespirationRate +
                     self.heatingRate(temperature) +
                     foragingRespirationRate)

    def growthRate(self):
        self.dGdt = 1

    ## HARVEST
    def nectarHarvestPotentialRate(self):
        # calculate maximum daily collection rate
        maxCollectionRateNectar = 1 #C_N

        ## Todo: determine environment and size driven function here
        workforceEffortN = self.density * self.foragingAllocationTrait * self.foragingEffortNectar # n_NF

        ## Potential resources-indpendent collection rate
        collectionRateNectar = maxCollectionRateNectar * workforceEffortN

        return(collectionRateNectar)

    def pollenHarvestPotentialRate(self):
        # calculate maximum daily collection rate
        maxCollectionRatePollen = 1  # C_N

        ## Todo: determine environment and size driven function here
        workforceEffortPollen = self.density * self.foragingAllocationTrait * self.foragingEffortPollen  # n_NF

        ## Potential resources-indpendent collection rate
        collectionRatePollen = maxCollectionRatePollen * workforceEffortPollen

        return (collectionRatePollen)

    def nectarHarvestRate(self, nectarResourcesRate):
        ## Todo:a should we add efficiency here? Or another conversion factor? Is this species dependent?
        self.dPndt = nectarResourcesRate - self.egestionNectarRate(nectarResourcesRate)

    def pollenHarvestRate(self, pollenResourceRate):
        ## Todo:a should we add efficiency here? Or another conversion factor? Is this species dependent?
        self.dPpdt = pollenResourceRate - self.egestionPollenRate(pollenResourceRate)



    def step(self, solver):
        # todo: implement order
        # assuming time = 1 day

        # assimilation
        ## todo: make sure reserves can't go below zero. Is there mortality factor associated with this?
        self.reservesNectar = self.reservesNectar + self.dPndt - self.dRdt
        self.reservesPollen = self.reservesPollen + self.dPndt

        # todo: fix reproduction
        # reproductive allocation
        self.reproduction = self.reproduction + self.dBdt - self.dMigdR

        # todo: add a link to migration somehow

        # todo: add a link from reproduction to somatic growth (i.e. new workers)
        # somatic growth
        self.density = self.density + self.dGdt - self.dMdt




    def print(self):
        print("Colony Pollinator")
        print(self.name)

def rungekutta4(dXdt, dt):
    k1 = 1
    k2 = 1
    k3 = 1
    k4 = 1
    return((k1 + 2*k2 + 2*k3 + k4)/6)