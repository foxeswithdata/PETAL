from abc import abstractmethod, ABC


class PlantBase(ABC):
    """Plant abstract base class"""

    @abstractmethod
    def initDensity(self):
        pass

    @abstractmethod
    def mortalityRate(self):
        pass

    @abstractmethod
    def growthRate(self):
        pass

    @abstractmethod
    def nectarProductionRate(self):
        pass

    @abstractmethod
    def pollenProductionRate(self):
        pass

    @abstractmethod
    def print(self):
        pass