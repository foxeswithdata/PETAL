import math
from petal.pollinator import PollinatorBase

"""
Module: colony_pollinator

Provides a simple ColonyPollinator class (subclassing PollinatorBase)
that implements a minimal set of state variables, rates and helper
methods used by the PETAL model for social/colony-forming pollinators
(e.g. bees with a worker caste).

Class: ColonyPollinator
Constructor arguments:
 - name: str
     Human-readable identifier for the colony.
 - foragingEffortNectar: float
     Relative effort allocated to nectar foraging (dimensionless, 0-1).
 - foragingEffortPollen: float
     Relative effort allocated to pollen foraging (dimensionless, 0-1).
 - foragingAllocationTrait: float
     Trait that scales workforce allocation to foraging (dimensionless).

Key state variables (attributes) and typical units or notes:
 - density: float
     Structural biomass / workforce size of the colony (gC m^-2 in code
     comments; treated as colony "size").
 - reservesNectar, reservesPollen: float
     Internal storage of nectar (sugar/carbon) and pollen (unitless or
     model units). Used for maintenance, reproduction and growth.
 - reproduction: float
     Cumulative reproduction/offspring state (model units).

Rate attributes (prefixed with d*dt) represent instantaneous rates
or fluxes (per day in the step-based implementation):
 - dGdt: growth rate (somatic growth, increases density)
 - dMdt: mortality rate (loss of density)
 - dBdt: birth/reproduction rate
 - dRdt: respiration rate (energy expenditure)
 - dMigdR: migration rate (loss/gain due to migration)

Collection and egestion rates:
 - dPndt, dPpdt: nectar and pollen harvest rates
 - dEndt, dEpdt: egestion of nectar and pollen (waste/loss)

Main methods (purpose):
 - mortalityRate(): compute and update self.dMdt
 - birthRate(): compute and update self.dBdt (placeholder)
 - respirationRate(temperature): compute/update self.dRdt
 - nectarHarvestPotentialRate(), pollenHarvestPotentialRate():
     compute resource-independent maximum collection given workforce
 - nectarHarvestRate(resourceRate), pollenHarvestRate(resourceRate):
     apply egestion and set actual harvest rates
 - step(solver): apply a single model time-step (assumes dt=1 day)

Notes and caveats:
 - Many methods are placeholders or contain TODOs. This module is a
   scaffold rather than a finished ecological model. Units for reserves,
   respiration and reproduction are not strictly defined in the code and
   should be harmonised with the rest of the PETAL model before use.
 - The built-in `defaultColonyPollinator()` convenience factory returns a
   ColonyPollinator with moderate default trait values.
"""

class ColonyPollinator(PollinatorBase):

    def __init__(self,
                 name,
                 foragingEffortNectar,
                 foragingEffortPollen,
                 foragingAllocationTrait,
                 nestWorkingAllocationTrait):

        ## traits
        self.name = name
        self.foragingEffortNectar = foragingEffortNectar                                       # Phi_N
        self.foragingEffortPollen = foragingEffortPollen                                       # Phi_P
        self.foragingAllocation = foragingAllocationTrait                                      # beta_F [dimensionless, 0-1]
        self.nestWorkingAllocation = nestWorkingAllocationTrait                                # beta_W [dimensionless, 0-1]
        self.reproductingAllocation = 1 - self.foragingAllocation - self.nestWorkingAllocation # beta_Q [dimensionless, 0-1]
        self.kappa = 1 # todo: determine how is Kappa calculated? permanent trait? or dynamic?  # kappa [dimensionless, 0-1]

        ## state variables
        # todo: determine how to handle density for colony pollinators. Should it be cohort based? E.g. cohorts of different sizes
        # of colonies and then density of those?
        self.adultBiomassDensity = 1 # V = V_F + V_W + V_Q [gC/m2] ; equivalent to structural biomass
        self.broodBiomassDensity = 1 # B [gC/m2]  ## equivalent to structural biomass

        self.reservesPollen = 0 # S_P [mgC/m2] ; Developing offspring: eggs, larvae, pupae
        self.reservesNectar = 0 # S_N [mgC/m2] ; Sugar-carbon for respiration, heating, flight


        # todo: figure out how to handle reproduction for colony pollinators.
        self.reproduction = 0 # todo: UNITS

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
        self.dENdt = 1 ## Egestion nectar rate
        self.dEPdt = 1 ## Egestion pollen rate

        # other
        self.nestTemperature = 0

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
    # todo write method description - this is the potential harvest rate given unlimited resources - also need to analyse this outside of the model
    def nectarHarvestPotentialRate(self, environment):
        # calculate maximum daily collection rate
        maxCollectionRateNectar = 1 #C_N

        # Todo: determine environment and size driven function here
        workforceEffortN = self.density * self.foragingAllocationTrait * self.foragingEffortNectar # n_NF

        ## Potential resources-indpendent collection rate
        collectionRateNectar = maxCollectionRateNectar * workforceEffortN

        return(collectionRateNectar)

    def pollenHarvestPotentialRate(self, environment):
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
        broodMaturityRate = 0.3
        newWorkers = self.reproduction * broodMaturityRate
        self.density = self.density + self.dGdt + newWorkers - self.dMdt




    def print(self):
        print("Colony Pollinator")
        print(self.name)

def rungekutta4(dXdt, dt):
    k1 = 1
    k2 = 1
    k3 = 1
    k4 = 1
    return((k1 + 2*k2 + 2*k3 + k4)/6)

def defaultColonyPollinator():
    defaultForagingEffortNectar = 0.5
    defaultForagingEffortPollen = 0.5
    defaultForagingAllocationTrait = 0.5
    default_colony_poll = ColonyPollinator(name="default",
                                           foragingEffortNectar=defaultForagingEffortNectar,
                                           foragingEffortPollen=defaultForagingEffortPollen,
                                           foragingAllocationTrait=defaultForagingAllocationTrait)
    return(default_colony_poll)