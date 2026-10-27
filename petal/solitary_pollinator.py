from petal.pollinator import PollinatorBase
import math

class SolitaryPollinator(PollinatorBase):

    def __init__(self,
                 name,
                 foragingEffortNectar,
                 foragingEffortPollen,
                 foragingAllocationTrait,
                 nestWorkingAllocationTrait,
                 kappa,
                 eclosionRateTrait,
                 massSpecificCollectingRateNectarTrait,
                 massSpecificCollectingRatePollenTrait,
                 egestionEfficiencyNectarTrait,
                 egestionEfficiencyPollenTrait,
                 maintenanceNectarRateTrait,
                 maintenancePollenRateTrait,
                 foragingMaintenanceRateTrait
                 ):
        ## traits
        self.name = name

        # Biomass/effort allocation traits
        self.foragingAllocation = foragingAllocationTrait  # beta_F [dimensionless, 0-1]
        self.nestWorkingAllocation = nestWorkingAllocationTrait  # beta_W [dimensionless, 0-1]
        self.reproductingAllocation = 1 - self.foragingAllocation - self.nestWorkingAllocation  # beta_Q [dimensionless, 0-1]

        self.kappa = kappa  # kappa [dimensionless, 0-1]
        self.eclosion_rate = eclosionRateTrait  # xi [d-1] ; proportion of brood that ecloses per day

        # Harvest and Foraging
        self.foragingEffortNectar = foragingEffortNectar  # Phi_N [dimensionless, 0-1]
        self.foragingEffortPollen = foragingEffortPollen  # Phi_P [dimensionless, 0-1]

        self.massSpecificCollectingRateNectar = massSpecificCollectingRateNectarTrait  # C_N [mgC/mgC/d] ; mass-specific nectar collection rate
        self.massSpecificCollectingRatePollen = massSpecificCollectingRatePollenTrait  # C_P [mgC/mgC/d] ; mass-specific pollen collection rate

        self.foragingDistanceMultiplier = 1  # lambda - no need to return to nest
        self.foragingMaintenanceRate = foragingMaintenanceRateTrait  # m_F [mgC/mgC/d] ; mass-specific foraging maintenance rate

        # Maintenance and egestion
        self.maintenanceNectarRate = maintenanceNectarRateTrait  # m_N [mgC/mgC/d] ; mass-specific nectar maintenance rate
        self.maintenancePollenRate = maintenancePollenRateTrait  # m_P [mgC/mgC/d] ; mass-specific pollen maintenance rate

        self.egestionNectarEfficiency = egestionEfficiencyNectarTrait  # epsilon_N [dimensionless, 0-1] ; fraction of nectar that is egested
        self.egestionPollenEfficiency = egestionEfficiencyPollenTrait  # epsilon_P [dimensionless, 0-1] ; fraction of pollen that is egested

        ## state variables
        # todo: determine how to handle density for colony pollinators. Should it be cohort based? E.g. cohorts of different sizes
        # of colonies and then density of those?
        self.adultBiomassDensity = 1  # V = V_F + V_W + V_Q [gC/m2] ; equivalent to structural biomass
        self.broodBiomassDensity = 0  # B [gC/m2]  ## equivalent to structural biomass always start at 0

        self.reservesPollen = 0  # S_P [mgC/m2] ; Developing offspring: eggs, larvae, pupae
        self.reservesNectar = 0  # S_N [mgC/m2] ; Sugar-carbon for respiration, heating, flight

        # todo: figure out how to handle reproduction for colony pollinators.
        self.reproduction = 0  # todo: UNITS

        # rates
        self.dGdt = 1  ## Growth rate
        self.dDdt = 1  ## mortality rate
        self.dBdt = 1  ## Birth/Reproduction rate
        self.dMNdt = 1  ## Maintenance rate nectar
        self.dMPdt = 1  ## Maintenance rate pollen
        self.dRNdt = 1  ## Respiration rate nectar
        self.dRPdt = 1  ## Respiration rate pollen
        self.dMFdt = 1  ## Maintenance rate foraging
        self.dMdt = 1  ## Maintenance rate
        self.dMigdR = 1  ## Migration rate

        ## collection
        self.dPndt = 1  ## Nectar harvest rate
        self.dPpdt = 1  ## Pollen harvest rate

        ## egestion
        self.dENdt = 1  ## Egestion nectar rate ; for reporting, don't actually use this in state change
        self.dEPdt = 1  ## Egestion pollen rate ; for reporting, don't actually use this in state change


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

    def foragingMaintenanceRate(self, environment):
        self.dMFdt = (self.foragingMaintenanceRate * self.foragingAllocation * self.adultBiomassDensity *
                  (self.foragingEffortNectar * self.spatialForagingEfficiencyNectar(environment) + self.foragingEffortPollen * self.spatialForagingEfficiencyPollen(environment)) *
                  self.foragingDistanceMultiplier)

    def egestionRateNectar(self):
        self.dENdt = self.dPndt * self.egestionNectarEfficiency

    def egestionRatePollen(self):
        self.dEPdt = self.dPpdt * self.egestionPollenEfficiency

    def respirationRatePollen(self, environment):
        # todo - maintenance of brood?
        self.dRPdt = self.maintenancePollenRate * self.adultBiomassDensity

    def respirationRateNectar(self, environment):
        # todo - maintenance of brood?
        self.dRNdt = self.maintenanceNectarRate * self.adultBiomassDensity

    def maintenanceRatePollen(self, environment):
        self.respirationRatePollen(environment)
        self.dMPdt = self.dRPdt

    def maintenanceRateNectar(self, environment):
        self.respirationRateNectar(environment)
        self.foragingMaintenanceRate(environment)
        self.dMNdt = self.dRNdt + self.dMFdt

    def maintenanceRate(self, environment):
        self.maintenanceRateNectar(environment)
        self.maintenanceRatePollen(environment)
        self.dMdt = (self.dMNdt + self.dMPdt)

    def growthRate(self):
        self.dGdt = 1

    ## HARVEST
    # equation number: 13
    # todo write method description - this is the potential harvest rate given total patch resources
    def nectarHarvestPotentialRate(self, totalNectarAvailable, environment):
        # calculate maximum daily collection rate
        workforceEffortNectar = self.massSpecificCollectingRateNectar * self.adultBiomassDensity * self.foragingAllocation * self.foragingEffortNectar * self.spatialForagingEfficiencyNectar(environment) # V_F,N

        ## Potential resources-indpendent collection rate
        collectionRateNectar = (totalNectarAvailable * workforceEffortNectar)/(totalNectarAvailable + workforceEffortNectar) * self.temperatureForagingEfficiency(environment)
        return(collectionRateNectar)

    def pollenHarvestPotentialRate(self, totalPollenAvailable, environment):
        workforceEffortPollen = self.massSpecificCollectingRatePollen * self.adultBiomassDensity * self.foragingAllocation * self.foragingEffortPollen  * self.spatialForagingEfficiencyPollen(environment) # n_NF

        ## Potential resources-indpendent collection rate
        collectionRatePollen = (totalPollenAvailable * workforceEffortPollen) / (totalPollenAvailable + workforceEffortPollen) * self.temperatureForagingEfficiency(environment)
        return (collectionRatePollen)

    def nectarHarvestRate(self, actualAvailableNectar):
        self.dPndt = actualAvailableNectar - self.egestionNectarRate(actualAvailableNectar)

    def pollenHarvestRate(self, actualAvailablePollen, environment):
        self.dPpdt = actualAvailablePollen - self.egestionPollenRate(actualAvailablePollen)

    ## todo implementation
    def spatialForagingEfficiencyNectar(self, environment):
        ## Todo: implement; future work
        return(1)

    def spatialForagingEfficiencyPollen(self, environment):
        ## Todo: implement; future work
        return(1)

    def temperatureForagingEfficiency(self, environment):
        ## Todo: implement; future work
        return(1)

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
        print("Solitary Pollinator")
        print(self.name)


def defaultSolitaryPollinator():
    defaultForagingEffortNectar = 0.5
    defaultForagingEffortPollen = 0.5
    defaultForagingAllocationTrait = 0.5
    defaultNestWorkingAllocationTrait = 0.25
    defaultKappa = 0.5
    defaultEclosionRateTrait = 0.1
    massSpecificCollectingRateNectarTrait = 1
    massSpecificCollectingRatePollenTrait = 1
    egestionEfficiencyNectarTrait = 0.05
    egestionEfficiencyPollenTrait = 0.3
    maintenanceNectarRateTrait = 0.1
    maintenancePollenRateTrait = 0.1
    foragingMaintenanceRateTrait = 0.1
    default_solitary_poll = SolitaryPollinator(name="default",
                                           foragingEffortNectar=defaultForagingEffortNectar,
                                           foragingEffortPollen=defaultForagingEffortPollen,
                                           foragingAllocationTrait=defaultForagingAllocationTrait,
                                           nestWorkingAllocationTrait=defaultNestWorkingAllocationTrait,
                                           kappa=defaultKappa,
                                           eclosionRateTrait=defaultEclosionRateTrait,
                                           massSpecificCollectingRateNectarTrait=massSpecificCollectingRateNectarTrait,
                                           massSpecificCollectingRatePollenTrait=massSpecificCollectingRatePollenTrait,
                                           egestionEfficiencyNectarTrait=egestionEfficiencyNectarTrait,
                                           egestionEfficiencyPollenTrait=egestionEfficiencyPollenTrait,
                                           maintenanceNectarRateTrait=maintenanceNectarRateTrait,
                                           maintenancePollenRateTrait=maintenancePollenRateTrait,
                                           foragingMaintenanceRateTrait=foragingMaintenanceRateTrait)
    return(default_solitary_poll)