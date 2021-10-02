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
                                                  'age': 0,
                                                  'target_x': np.nan,
                                                   'target_y': np.nan})
        self._logger = logging.getLogger(__name__)
        self._logger.debug(f"Initiating {self.name}")

    def random_move(self, aimless_herbivores):
        x_movement_vector = [random.uniform(-50, 50) for i in range(aimless_herbivores.shape[0])]
        y_movement_vector = [random.uniform(-50, 50) for i in range(aimless_herbivores.shape[0])]
        aimless_herbivores.x = aimless_herbivores.x + (x_movement_vector * aimless_herbivores.speed)
        aimless_herbivores.y = aimless_herbivores.y + (y_movement_vector * aimless_herbivores.speed)
        aimless_herbivores.x[aimless_herbivores.x < 0] = 0 + 5
        aimless_herbivores.y[aimless_herbivores.y < 0] = 0 + 5
        aimless_herbivores.x[aimless_herbivores.x > self.envsize] = self.envsize - 5
        aimless_herbivores.y[aimless_herbivores.y > self.envsize] = self.envsize - 5
        return aimless_herbivores

    def aimed_move(self, aimed_herbivores):
        aimed_herbivores.x = aimed_herbivores.x + (((aimed_herbivores.target_x - aimed_herbivores.x) / 25) * aimed_herbivores.speed)
        aimed_herbivores.y = aimed_herbivores.y + (((aimed_herbivores.target_y - aimed_herbivores.y) / 25) * aimed_herbivores.speed)
        return aimed_herbivores

    def move(self):
        aimless_herbivores = self.herbivore_population.loc[self.herbivore_population['target_x'] == -100]
        aimless_herbivores = self.random_move(aimless_herbivores)
        aimed_herbivores = self.herbivore_population.loc[self.herbivore_population['target_x'] != -100]
        aimed_herbivores = self.aimed_move(aimed_herbivores)
        self.herbivore_population = pd.concat([aimed_herbivores, aimless_herbivores])

    def eat(self, plants):
        eaten_plants = plants.loc[plants['dist'] < 50.0]
        non_eaten_plants = plants.loc[plants['dist'] > 50.0]
        hungry_herbivores = self.herbivore_population.loc[~self.herbivore_population.index.isin(eaten_plants.index)]
        eating_herbivores = self.herbivore_population.loc[self.herbivore_population.index.isin(eaten_plants.index)]
        eating_herbivores['energy'] = eating_herbivores['energy'] + (eaten_plants['size'] * 1)
        eating_herbivores['target_x'] = -100
        eating_herbivores['target_y'] = -100
        hungry_herbivores = self.select_target(hungry_herbivores, non_eaten_plants)
        self.herbivore_population = pd.concat([hungry_herbivores, eating_herbivores]).reset_index(drop=True)

    def select_target(self, hungry_herbivores, plants):
        hungry_herbivores['target_x'] = plants['x']
        hungry_herbivores['target_y'] = plants['y']
        return hungry_herbivores

    def age(self):
        self.herbivore_population['age'] = self.herbivore_population['age'] + 1
        self.herbivore_population['energy'] = self.herbivore_population['energy'] - 0.1
        self.reproduce()
        self.kill_old()
        self.starve()

    def kill_old(self):
        self.herbivore_population = self.herbivore_population.loc[self.herbivore_population['age'] < 50]

    def starve(self):
        self.herbivore_population = self.herbivore_population.loc[self.herbivore_population['energy'] > 0]

    def reproduce(self):
        reproducing_individuals = self.herbivore_population.loc[self.herbivore_population['energy'] > 8]
        babies = reproducing_individuals.copy()
        non_repoducing_individuals = self.herbivore_population.loc[~self.herbivore_population.index.isin(reproducing_individuals.index)]
        babies['x'] = babies['x'] + random.uniform(-5, 5)
        babies['y'] = babies['y'] + random.uniform(-5, 5)
        babies['size'] = babies['speed'] + random.uniform(-0.1, 0.1)
        babies['reproduction_rate'] = babies['reproduction_rate'] + random.uniform(-0.1, 0.1)
        babies['energy'] = 5
        babies['age'] = 0
        reproducing_individuals['energy'] = reproducing_individuals['energy'] - 5
        self.herbivore_population = pd.concat([babies, reproducing_individuals, non_repoducing_individuals]).reset_index(drop=True)