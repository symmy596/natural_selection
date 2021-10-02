import logging
import random
import pandas as pd
import numpy as np


class Plant:
    name = "plant"
    plant_population = pd.DataFrame

    def __init__(self, nplants, envsize):
        self.nplants = nplants
        self.envsize = envsize
        x = [random.uniform(0, self.envsize) for i in range(self.nplants)]
        y = [random.uniform(0, self.envsize) for i in range(self.nplants)]
        size = np.random.uniform(0, 5, self.nplants)
        reproduction_rate = np.random.uniform(0, 0.1, self.nplants)
        self.plant_population = pd.DataFrame({'x': x,
                                              'y': y,
                                              'size': size,
                                              'reproduction_rate': reproduction_rate})

        self._logger = logging.getLogger(__name__)
        self._logger.debug(f"Initiating {self.name}")

    def grow_plants(self):
        self.plant_population['random_chance'] = np.random.uniform(0, 1, self.plant_population.shape[0])
        self.plant_population['reproduction_chance'] = self.plant_population['reproduction_rate'] + self.plant_population['random_chance']
        reproducing_plants = self.plant_population.nlargest(int(self.nplants / 20), 'reproduction_chance')
        reproducing_plants['x'] = reproducing_plants['x'] + random.uniform(-5, 5)
        reproducing_plants['y'] = reproducing_plants['y'] + random.uniform(-5, 5)
        reproducing_plants['size'] = reproducing_plants['size'] + random.uniform(-0.1, 0.1)
        reproducing_plants['reproduction_rate'] = reproducing_plants['reproduction_rate'] + random.uniform(-0.1, 0.1)
        self.plant_population = pd.concat([self.plant_population, reproducing_plants]).reset_index(drop=True)
        self.plant_population.drop(columns=['reproduction_chance', 'random_chance'])
        self.nplants = self.plant_population.shape[0]

    def die(self, distances):
        eaten_plants = distances.loc[distances['dist'] < 50.0]
        self.plant_population = self.plant_population.loc[~self.plant_population.index.isin(eaten_plants.index)]

