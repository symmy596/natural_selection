import logging
import random
import pandas as pd
import numpy as np


class Herbivore:
    herbivore_population = pd.DataFrame
    name = "herbivore"
    herbivore_properties = [{'color': 'blue', 'speed': 1, 'breeding_threshold': 5}]
    def __init__(self, nherbivores, envsize):
        self.nherbivores = nherbivores
        self.envsize = envsize
        x = [random.uniform(0, self.envsize) for i in range(self.nherbivores)]
        y = [random.uniform(0, self.envsize) for i in range(self.nherbivores)]
        reproduction_rate = [0.5 for i in range(self.nherbivores)]
        speed = [random.choice(self.herbivore_properties)['speed'] for i in range(self.nherbivores)]
        self.herbivore_population = pd.DataFrame({'x': x,
                                                  'y': y,
                                                  'speed': speed,
                                                  'reproduction_rate': reproduction_rate,
                                                  'energy': 5,
                                                  'age': 0})
        self._logger = logging.getLogger(__name__)
        self._logger.debug(f"Initiating {self.name}")

    def move(self):
        x_movement_vector = [random.uniform(-50, 50) for i in range(self.herbivore_population.shape[0])]
        y_movement_vector = [random.uniform(-50, 50) for i in range(self.herbivore_population.shape[0])]
        self.herbivore_population.x = self.herbivore_population.x + (x_movement_vector * self.herbivore_population.speed)
        self.herbivore_population.y = self.herbivore_population.y + (y_movement_vector * self.herbivore_population.speed)
        self.herbivore_population.x[self.herbivore_population.x < 0] = 0 + 5
        self.herbivore_population.y[self.herbivore_population.y < 0] = 0 + 5
        self.herbivore_population.x[self.herbivore_population.x > self.envsize] = self.envsize - 5
        self.herbivore_population.y[self.herbivore_population.y > self.envsize] = self.envsize - 5

    def eat(self, indexes, plant_sizes):
        hungry_herbivores = self.herbivore_population.loc[~self.herbivore_population.index.isin(indexes)]
        eating_herbivores = self.herbivore_population.loc[self.herbivore_population.index.isin(indexes)]
        eating_herbivores['energy'] = eating_herbivores['energy'] + plant_sizes
        self.herbivore_population = pd.concat([hungry_herbivores, eating_herbivores]).reset_index(drop=True)

    def age(self):
        self.herbivore_population['age'] = self.herbivore_population['age'] + 1
        self.kill_old()
        self.starve()

    def kill_old(self):
        self.herbivore_population = self.herbivore_population.loc[self.herbivore_population['age'] < 50]

    def starve(self):
        self.herbivore_population = self.herbivore_population.loc[self.herbivore_population['energy'] > 0]

