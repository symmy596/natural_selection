import logging
import random
import pandas as pd


class Herbivore:
    herbivore_population = pd.DataFrame
    name = "herbivore"

    def __init__(self, nherbivores, envsize):
        self.nherbivores = nherbivores
        self.envsize = envsize
        self.x = [random.uniform(0, self.envsize) for i in range(self.nherbivores)]
        self.y = [random.uniform(0, self.envsize) for i in range(self.nherbivores)]
        self.reproduction_rate = [0.5 for i in range(self.nherbivores)]
        self.herbivore_population = pd.DataFrame({'x': self.x,
                                              'y': self.y,
                                              'reproduction_rate': self.reproduction_rate})
        self._logger = logging.getLogger(__name__)
        self._logger.debug(f"Initiating {self.name}, {self.x}, {self.y}")
        self._logger = logging.getLogger(__name__)

    def move(self):
        pass

    def breed(self):
        pass

    def eat(self):
        pass

    def die(self):
        pass
