import logging
import random
import pandas as pd
import numpy as np


class Herbivore:
    herbivore_population = pd.DataFrame
    name = "herbivore"
    eating_radius = 10

    def __init__(self, herbivore_properties, envsize):
        self.herbivore_properties = herbivore_properties
        self.envsize = envsize
        # TODO These need to be set in the simulation parameters
        x = np.random.uniform(
            0, self.envsize, self.herbivore_properties["starting_number"]
        )
        y = np.random.uniform(
            0, self.envsize, self.herbivore_properties["starting_number"]
        )
        speed = np.random.uniform(
            self.herbivore_properties["speed"][0],
            self.herbivore_properties["speed"][1],
            self.herbivore_properties["starting_number"],
        )
        life_expectancy = np.random.uniform(
            self.herbivore_properties["life_expectancy"][0],
            self.herbivore_properties["life_expectancy"][1],
            self.herbivore_properties["starting_number"],
        )
        reproduction_energy = np.random.uniform(
            self.herbivore_properties["reproduction_energy"][0],
            self.herbivore_properties["reproduction_energy"][1],
            self.herbivore_properties["starting_number"],
        )
        size = np.random.uniform(
            self.herbivore_properties["size"][0],
            self.herbivore_properties["size"][1],
            self.herbivore_properties["starting_number"],
        )
        perception = np.random.uniform(
            self.herbivore_properties['perception'][0],
            self.herbivore_properties['perception'][1],
            self.herbivore_properties['starting_number']
        )
        self.herbivore_population = pd.DataFrame(
            {
                "x": x,
                "y": y,
                "speed": speed,
                "life_expectancy": life_expectancy,
                "reproduction_energy": reproduction_energy,
                "perception": perception,
                "movesize": self.herbivore_properties["movesize"],
                "size": size,
                "energy": self.herbivore_properties["starting_energy"],
                "age": 0,
                "nearest_plant_x": np.nan,
                "nearest_plant_y": np.nan,
                "nearest_neighbour_distance": np.nan,
                "nearest_neighbour_index": np.nan,
                "nearest_neighbour_size": np.nan,
                "target": False,
                "x_hunt_time": 0,
                "y_hunt_time": 0,
            }
        )
        self.movesizes = [-self.herbivore_properties['movesize'], self.herbivore_properties['movesize']]
        self._logger = logging.getLogger(__name__)
        self._logger.debug(f"Initiating {self.name}")

    def random_move(self, aimless_herbivores):
        self._logger.info(aimless_herbivores)
        #TODO Clever relationship needed
        aimless_herbivores["x"] = aimless_herbivores["x"] + (random.choice(self.movesizes)
            * (aimless_herbivores["size"] * aimless_herbivores["speed"])
        )
        aimless_herbivores["y"] = aimless_herbivores["y"] + (random.choice(self.movesizes)
            * (aimless_herbivores["size"] * aimless_herbivores["speed"])
        )
        aimless_herbivores["x"][aimless_herbivores["x"] < 0] = 0 + 5
        aimless_herbivores["y"][aimless_herbivores["y"] < 0] = 0 + 5
        aimless_herbivores["x"][aimless_herbivores["x"] > self.envsize] = (
            self.envsize - 5
        )
        aimless_herbivores["y"][aimless_herbivores["y"] > self.envsize] = (
            self.envsize - 5
        )
        return aimless_herbivores

    def aimed_move(self, aimed_herbivores):
        #TODO Clever relationship needed
        aimed_herbivores["x"] = aimed_herbivores["x"] + (
            ((aimed_herbivores["nearest_plant_x"] - aimed_herbivores["x"]) / 2)
            * (aimed_herbivores["size"] * aimed_herbivores["speed"])
        )
        aimed_herbivores["y"] = aimed_herbivores["y"] + (
            ((aimed_herbivores["nearest_plant_y"] - aimed_herbivores["y"]) / 2)
            * (aimed_herbivores["size"] * aimed_herbivores["speed"])
        )
        return aimed_herbivores

    def move(self):
        aimless_herbivores = self.herbivore_population.loc[
            self.herbivore_population["target"] == False
        ]
        aimless_herbivores = self.random_move(aimless_herbivores)
        aimed_herbivores = self.herbivore_population.loc[
            self.herbivore_population["target"] == True
        ]
        aimed_herbivores = self.aimed_move(aimed_herbivores)
        self.herbivore_population = pd.concat([aimed_herbivores, aimless_herbivores])

    def select_target(self, hungry_herbivores):
        targetted_herbivores = hungry_herbivores.loc[hungry_herbivores['target'] == True]
        non_targetted_herbivores = hungry_herbivores.loc[hungry_herbivores['target'] == False]
        far_away_plants = non_targetted_herbivores.query("dist > perception")
        close_to_plants = non_targetted_herbivores.query("dist < perception")
        close_to_plants['target'] = True
        close_to_plants['x_hunt_time'] = 4
        close_to_plants['y_hunt_time'] = 4
        hungry_herbivores = pd.concat(
            [targetted_herbivores, far_away_plants, close_to_plants]
        ).reset_index(drop=True)
        return hungry_herbivores

    def eat(self):
        hungry_herbivores = self.herbivore_population.loc[self.herbivore_population['dist'] > self.eating_radius]
        eating_herbivores = self.herbivore_population.loc[self.herbivore_population['dist'] < self.eating_radius]
        #TODO Clever relationship needed
        eating_herbivores["energy"] = eating_herbivores["energy"] + eating_herbivores["nearest_neighbour_size"]
        eating_herbivores["nearest_plant_x"] = -100
        eating_herbivores["nearest_plant_x"] = -100
        hungry_herbivores = self.select_target(hungry_herbivores)
        self.herbivore_population = pd.concat(
            [hungry_herbivores, eating_herbivores]
        ).reset_index(drop=True)

    def age(self):
        self.herbivore_population["age"] = self.herbivore_population["age"] + 1
        #TODO Clever relationship needed
        self.herbivore_population["energy"] = self.herbivore_population["energy"] - 1
        self.reproduce()
        self.kill_old()
        self.starve()

    def kill_old(self):
        dead_herbivores = self.herbivore_population.query("age > life_expectancy")
        self.herbivore_population = self.herbivore_population.loc[
            ~self.herbivore_population.index.isin(dead_herbivores.index)
        ]

    def starve(self):
        self.herbivore_population = self.herbivore_population.loc[
            self.herbivore_population["energy"] > 0
        ]

    def reproduce(self):
        reproducing_individuals = self.herbivore_population.query(
            "energy > reproduction_energy"
        )
        babies = reproducing_individuals.copy()
        non_repoducing_individuals = self.herbivore_population.loc[
            ~self.herbivore_population.index.isin(reproducing_individuals.index)
        ]
        babies["x"] = babies["x"] + random.uniform(-15, 15)
        babies["y"] = babies["y"] + random.uniform(-15, 15)
        babies["size"] = babies["speed"] + random.uniform(
            -self.herbivore_properties["mutation_rate"],
            self.herbivore_properties["mutation_rate"],
        )
        babies["life_expectancy"] = babies["life_expectancy"] + random.uniform(
            -self.herbivore_properties["mutation_rate"],
            self.herbivore_properties["mutation_rate"],
        )
        babies["reproduction_energy"] = babies["reproduction_energy"] + random.uniform(
            -self.herbivore_properties["mutation_rate"],
            self.herbivore_properties["mutation_rate"],
        )
        babies["speed"] = babies["speed"] + random.uniform(
            -self.herbivore_properties["mutation_rate"],
            self.herbivore_properties["mutation_rate"],
        )
        babies["movesize"] = babies["movesize"] + random.uniform(
            -self.herbivore_properties["mutation_rate"],
            self.herbivore_properties["mutation_rate"],
        )
        babies["size"] = babies["size"] + random.uniform(
            -self.herbivore_properties["mutation_rate"],
            self.herbivore_properties["mutation_rate"],
        )
        babies['perception'] = babies["perception"] + random.uniform(
            -self.herbivore_properties["mutation_rate"],
            self.herbivore_properties["mutation_rate"],
        )
        babies["nearest_plant_x"] = -100
        babies["nearest_plant_y"] = -100
        babies["nearest_neighbour_distance"] = np.nan
        babies["nearest_neighbour_index"] = np.nan
        babies["nearest_neighbour_size"] = np.nan
        babies["target"] = False
        babies["x_hunt_time"] = 0
        babies["y_hunt_time"] = 0
        babies["energy"] = self.herbivore_properties["starting_energy"]
        babies["age"] = 0
        babies["target_x"] = -100
        babies["target_y"] = -100
        reproducing_individuals["energy"] = self.herbivore_properties["starting_energy"]
        self.herbivore_population = pd.concat(
            [babies, reproducing_individuals, non_repoducing_individuals]
        ).reset_index(drop=True)
