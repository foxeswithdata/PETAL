from petal.pollinator import PollinatorBase


class SolitaryPollinator(PollinatorBase):

    def __init__(self):
        self.dGdt = 1
        self.dMdt = 1
        self.dBdt = 1
        print("Hello World")

    def mortalityRate(self):
        print("Hello World")

    def growthRate(self):
        print("Hello World")

    def birthRate(self):
        print("Hello World")

