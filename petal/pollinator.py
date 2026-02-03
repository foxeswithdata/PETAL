from abc import abstractmethod, ABC


class PollinatorBase(ABC):
    """Pollinator abstract base class"""


    @abstractmethod
    def mortalityRate(self):
        pass

    @abstractmethod
    def birthRate(self):
        pass

    @abstractmethod
    def growRate(self):
        pass

    @abstractmethod
    def print(self):
        pass

