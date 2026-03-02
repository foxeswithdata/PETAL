from abc import abstractmethod, ABC


class PollinatorBase(ABC):
    """Pollinator abstract base class"""

    @abstractmethod
    def initDensity(self):
        pass

    @abstractmethod
    def mortalityRate(self):
        pass

    @abstractmethod
    def birthRate(self):
        pass

    @abstractmethod
    def growthRate(self):
        pass

    @abstractmethod
    def print(self):
        pass

