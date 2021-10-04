import logging
import random
import pandas as pd
import numpy as np


class Herbivore:
    herbivore_population = pd.DataFrame
    name = "herbivore"
    def __init__(self, herbivore_properties, envsize):
        self.herbivore_properties = herbivore_properties
        self.envsize = envsize
        #TODO These need to be set in the simulation parameters
        x = np.random.uniform(0, self.envsize, self.herbivore_properties['starting_number'])
        y = np.random.uniform(0, self.envsize, self.herbivore_properties['starting_number'])
        speed = np.random.uniform(self.herbivore_properties['speed'][0],
                                  self.herbivore_properties['speed'][1],
                                  self.herbivore_properties['starting_number'])
        life_expectancy = np.random.uniform(self.herbivore_properties['life_expectancy'][0],
                                            self.herbivore_properties['life_expectancy'][1],
                                            self.herbivore_properties['starting_number'])
        reproduction_energy = np.random.uniform(self.herbivore_properties['reproduction_energy'][0],
                                                self.herbivore_properties['reproduction_energy'][1],
                                                self.herbivore_properties['starting_number'])
        movesize = np.random.uniform(self.herbivore_properties['movesize'][0],
                                     self.herbivore_properties['movesize'][1],
                                     self.herbivore_properties['starting_number'])
        self.herbivore_population = pd.DataFrame({'x': x,
                                                  'y': y,
                                                  'speed': speed,
                                                  'life_expectancy': life_expectancy,
                                                  'reproduction_energy': reproduction_energy,
                                                  'movesize': movesize,
                                                  'size': self.herbivore_properties['starting_energy'],
                                                  'age': 0,
                                                  'target_x': np.nan,
                                                  'target_y': np.nan})
        self._logger = logging.getLogger(__name__)
        self._logger.debug(f"Initiating {self.name}")


    def random_move(self, aimless_herbivores):
        aimless_herbivores['x'] = aimless_herbivores['x'] + (aimless_herbivores['movesize'] + (aimless_herbivores['size'] / aimless_herbivores['speed']))
        aimless_herbivores['y'] = aimless_herbivores['y'] + (aimless_herbivores['movesize'] + (aimless_herbivores['size'] / aimless_herbivores['speed']))
        aimless_herbivores['x'][aimless_herbivores['x'] < 0] = 0 + 5
        aimless_herbivores['y'][aimless_herbivores['y'] < 0] = 0 + 5
        aimless_herbivores['x'][aimless_herbivores['x'] > self.envsize] = self.envsize - 5
        aimless_herbivores['y'][aimless_herbivores['y'] > self.envsize] = self.envsize - 5
        return aimless_herbivores

    def aimed_move(self, aimed_herbivores):
        aimed_herbivores['x'] = aimed_herbivores['x'] + (((aimed_herbivores['target_x'] - aimed_herbivores['x']) / 4) + (aimed_herbivores['size'] / aimed_herbivores['speed']))
        aimed_herbivores['y'] = aimed_herbivores['y'] + (((aimed_herbivores['target_y'] - aimed_herbivores['y']) / 4) + (aimed_herbivores['size'] / aimed_herbivores['speed']))
        return aimed_herbivores

    def move(self):
        aimless_herbivores = self.herbivore_population.loc[self.herbivore_population['target_x'] == -100]
        aimless_herbivores = self.random_move(aimless_herbivores)
        aimed_herbivores = self.herbivore_population.loc[self.herbivore_population['target_x'] != -100]
        aimed_herbivores = self.aimed_move(aimed_herbivores)
        self.herbivore_population = pd.concat([aimed_herbivores, aimless_herbivores])

    def eat(self, plants):
        eaten_plants = plants.loc[plants['dist'] < 10.0]
        non_eaten_plants = plants.loc[plants['dist'] > 10.0]
        hungry_herbivores = self.herbivore_population.loc[~self.herbivore_population.index.isin(eaten_plants.index)]
        eating_herbivores = self.herbivore_population.loc[self.herbivore_population.index.isin(eaten_plants.index)]
        eating_herbivores['size'] = eating_herbivores['size'] + eaten_plants['size']
        eating_herbivores['target_x'] = -100
        eating_herbivores['target_y'] = -100
        hungry_herbivores = self.select_target(hungry_herbivores, non_eaten_plants)
        self.herbivore_population = pd.concat([hungry_herbivores, eating_herbivores]).reset_index(drop=True)

    def select_target(self, hungry_herbivores, plants):
        plants['dist'] = plants['dist'] / plants['size']
        #TODO Build perception metric here
        #TODO I wrote this function after 8 beers and I don't entirely know what it is doing. Figure this out
        nearby_plants = plants.loc[plants['dist'] < 10]
        targetted_herbivores = hungry_herbivores.loc[hungry_herbivores.index.isin(nearby_plants.index)]
        far_away_plants = plants.loc[~plants.index.isin(nearby_plants.index)]
        non_targetted_herbivores = hungry_herbivores.loc[hungry_herbivores.index.isin(far_away_plants.index)]
        targetted_herbivores['target_x'] = nearby_plants['x']
        targetted_herbivores['target_y'] = nearby_plants['y']
        non_targetted_herbivores['target_x'] = -100
        non_targetted_herbivores['target_y'] = -100
        hungry_herbivores = pd.concat([non_targetted_herbivores, targetted_herbivores]).reset_index(drop=True)
        return hungry_herbivores

    def age(self):
        self.herbivore_population['age'] = self.herbivore_population['age'] + 1
        self.herbivore_population['size'] = self.herbivore_population['size'] - (self.herbivore_population['speed'] / 2)
        self.reproduce()
        self.kill_old()
        self.starve()

    def kill_old(self):
        dead_herbivores = self.herbivore_population.query('age > life_expectancy')
        self.herbivore_population = self.herbivore_population.loc[~self.herbivore_population.index.isin(dead_herbivores.index)]

    def starve(self):
        self.herbivore_population = self.herbivore_population.loc[self.herbivore_population['size'] > 0]

    def reproduce(self):
        reproducing_individuals = self.herbivore_population.query('size > reproduction_energy')
        babies = reproducing_individuals.copy()
        non_repoducing_individuals = self.herbivore_population.loc[~self.herbivore_population.index.isin(reproducing_individuals.index)]
        babies['x'] = babies['x'] + random.uniform(-15, 15)
        babies['y'] = babies['y'] + random.uniform(-15, 15)
        babies['size'] = babies['speed'] + random.uniform(-self.herbivore_properties['mutation_rate'],
                                                          self.herbivore_properties['mutation_rate'])
        babies['life_expectancy'] = babies['life_expectancy'] + random.uniform(-self.herbivore_properties['mutation_rate'],
                                                                               self.herbivore_properties['mutation_rate'])
        babies['reproduction_energy'] = babies['reproduction_energy'] + random.uniform(-self.herbivore_properties['mutation_rate'],
                                                                                       self.herbivore_properties['mutation_rate'])
        babies['speed'] = babies['speed'] + random.uniform(-self.herbivore_properties['mutation_rate'],
                                                           self.herbivore_properties['mutation_rate'])
        babies['movesize'] = babies['movesize'] + random.uniform(-self.herbivore_properties['mutation_rate'],
                                                                 self.herbivore_properties['mutation_rate'])
        babies['size'] = 5
        babies['age'] = 0
        babies['target_x'] = -100
        babies['target_y'] = -100
        reproducing_individuals['size'] = 5
        self.herbivore_population = pd.concat([babies, reproducing_individuals, non_repoducing_individuals]).reset_index(drop=True)