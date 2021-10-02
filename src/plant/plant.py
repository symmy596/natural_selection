import logging
import random
import pandas as pd

class Plant:
    name = "plant"
    potential_properties = [{'color': 'green', 'reproduction_rate': 0.6, 'size': 5},
                            {'color': 'red', 'reproduction_rate': 0.61, 'size': 2}]
    plant_population = pd.DataFrame

    def __init__(self, nplants, envsize):
        self.nplants = nplants
        self.envsize = envsize
        x = [random.uniform(0, self.envsize) for i in range(self.nplants)]
        y = [random.uniform(0, self.envsize) for i in range(self.nplants)]
        size = [random.choice(self.potential_properties)['size']  for i in range(self.nplants)]
        color = [random.choice(self.potential_properties)['color'] for i in range(self.nplants)]
        reproduction_rate = [random.choice(self.potential_properties)['reproduction_rate']  for i in range(self.nplants)]
        self.plant_population = pd.DataFrame({'x': x,
                                              'y': y,
                                              'size': size,
                                              'color': color,
                                              'reproduction_rate': reproduction_rate})

        self._logger = logging.getLogger(__name__)
        self._logger.debug(f"Initiating {self.name}")

    def grow_plants(self):
        self.plant_population['random_chance'] = [random.uniform(0, 1) for i in range(len((self.plant_population.x)))]
        self.plant_population['reproduction_chance'] = self.plant_population['reproduction_rate'] + self.plant_population['random_chance']
        reproducing_plants = self.plant_population.loc[self.plant_population['reproduction_chance'] > 1.60]
        reproducing_plants['x'] = reproducing_plants['x'] + random.uniform(-5, 5)
        reproducing_plants['y'] = reproducing_plants['y'] + random.uniform(-5, 5)
        self.plant_population = pd.concat([self.plant_population, reproducing_plants]).reset_index(drop=True)
        self.plant_population.drop(columns=['reproduction_chance', 'random_chance'])

    def die(self, eaten_indexes):
        self.plant_population = self.plant_population.loc[~self.plant_population.index.isin(eaten_indexes)]

