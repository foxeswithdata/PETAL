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
        self.density = 1 # gC/m2

        self.reservesPollen = 0
        self.reservesNectar = 0

        # rates
        self.dGdt = 1 ## Growth rate
        self.dMdt = 1 ## mortality rate
        self.dBdt = 1 ## Birth/Reproduction rate
        self.dRdt = 1 ## Respiration rate

        ## collection
        self.dPndt = 1 ## Nectar harvest rate
        self.dPpdt = 1 ## Pollen harvest rate

        ## egestion
        self.dEndt = 1 ## Egestion nectar rate
        self.dEpdt = 1 ## Egestion pollen rate

    def initDensity(self):
        print("Hello World")

    def mortalityRate(self):
        print("Hello World")

    def growthRate(self):
        print("Hello World")

    def birthRate(self):
        print("Hello World")

    def heatingRate(self):
        print("Hello World")

    def flightCost(self):
        print("Hello World")

    def egestionNectarRate(self):
        egestionNectar = 1
        self.dEndt = 1

    def egestionPollenRate(self):
        egestionPollen = 1
        self.dEpdt = 1

    def respirationRate(self, temperature):
        somaticMaintenanceRespirationRate = 1
        foragingRespirationRate = 1
        self.dRdt = somaticMaintenanceRespirationRate + self.heatingRate(temperature) + foragingRespirationRate

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
        self.dPndt = nectarResourcesRate

    def pollenHarvestRate(self, pollenResourceRate):
        self.dPpdt = pollenResourceRate

    def print(self):
        print("Colony Pollinator")
        print(self.name)

