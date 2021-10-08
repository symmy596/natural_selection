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
            self.herbivore_properties["perception"][0],
            self.herbivore_properties["perception"][1],
            self.herbivore_properties["starting_number"],
        )
        perception_radius = perception * 10
        max_movesize = (
            (np.power(speed, 3)) - (np.power(size, 2))
        ) / self.herbivore_properties["movesize"]
        self.herbivore_population = pd.DataFrame(
            {
                "x": x,
                "y": y,
                "speed": speed,
                "perception": perception,
                "size": size,
                "life_expectancy": life_expectancy,
                "reproduction_energy": reproduction_energy,
                "energy": self.herbivore_properties["starting_energy"],
                "age": 0,
                "perception_radius": perception_radius,
                "max_movesize": max_movesize,
                "nearest_plant_x": np.nan,
                "nearest_plant_y": np.nan,
                "nearest_neighbour_distance": np.nan,
                "nearest_neighbour_index": np.nan,
                "nearest_neighbour_size": np.nan,
                "target": False,
            }
        )
        self.movesizes = np.arange(-self.herbivore_properties["movesize"], self.herbivore_properties["movesize"], 10)
        self._logger = logging.getLogger(__name__)
        self._logger.debug(f"Initiating {self.name}")

    def random_move(self, aimless_herbivores):
        aimless_herbivores["x"] = aimless_herbivores["x"] + (
            (
                np.power(aimless_herbivores["speed"], 3)
                - np.power(aimless_herbivores["speed"], 2)
            )
            / random.choice(self.movesizes)
        )
        aimless_herbivores["y"] = aimless_herbivores["y"] + (
            (
                np.power(aimless_herbivores["speed"], 3)
                - np.power(aimless_herbivores["speed"], 2)
            )
            / random.choice(self.movesizes)
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
        outside_range = aimed_herbivores.query(
            "nearest_neighbour_distance > max_movesize"
        )
        inside_range = aimed_herbivores.query(
            "nearest_neighbour_distance < max_movesize"
        )
        inside_range["x"] = inside_range["nearest_plant_x"].copy() + 2
        inside_range["y"] = inside_range["nearest_plant_y"].copy() + 2
        outside_range["x"] = outside_range["x"] + np.copysign(
            outside_range["max_movesize"],
            (outside_range["nearest_plant_x"] - outside_range["x"]),
        )
        outside_range["y"] = outside_range["y"] + np.copysign(
            outside_range["max_movesize"],
            (outside_range["nearest_plant_y"] - outside_range["y"]),
        )
        aimed_herbivores = pd.concat([inside_range, outside_range]).reset_index(
            drop=True
        )
        return aimed_herbivores

    def move(self):
        #TODO x,y need to not be the same
        aimless_herbivores = self.herbivore_population.loc[
            self.herbivore_population["target"] == False
        ]
        aimless_herbivores = self.random_move(aimless_herbivores)
        aimed_herbivores = self.herbivore_population.loc[
            self.herbivore_population["target"] == True
        ]
        aimed_herbivores = self.aimed_move(aimed_herbivores)
        self.herbivore_population = pd.concat(
            [aimed_herbivores, aimless_herbivores]
        ).reset_index(drop=True)

    def select_target(self, hungry_herbivores):
        targetted_herbivores = hungry_herbivores.loc[
            hungry_herbivores["target"] == True
        ]
        non_targetted_herbivores = hungry_herbivores.loc[
            hungry_herbivores["target"] == False
        ]
        far_away_plants = non_targetted_herbivores.query(
            "nearest_neighbour_distance > perception_radius"
        )
        close_to_plants = non_targetted_herbivores.query(
            "nearest_neighbour_distance < perception_radius"
        )
        close_to_plants["target"] = True
        hungry_herbivores = pd.concat(
            [targetted_herbivores, far_away_plants, close_to_plants]
        ).reset_index(drop=True)
        return hungry_herbivores

    def eat(self):
        hungry_herbivores = self.herbivore_population.loc[
            self.herbivore_population["nearest_neighbour_distance"] > self.eating_radius
        ]
        eating_herbivores = self.herbivore_population.loc[
            self.herbivore_population["nearest_neighbour_distance"] < self.eating_radius
        ]
        eating_herbivores = eating_herbivores.sort_values('size', ascending=False)
        lucky_herbivores = eating_herbivores.drop_duplicates(subset=['nearest_neighbour_index'])
        unlucky_herbivores = eating_herbivores.loc[~eating_herbivores.index.isin(lucky_herbivores.index)]

        lucky_herbivores["energy"] = (
            lucky_herbivores["energy"] + lucky_herbivores["nearest_neighbour_size"]
        )
        eating_herbivores = pd.concat([lucky_herbivores, unlucky_herbivores])
        eating_herbivores["nearest_plant_x"] = np.nan
        eating_herbivores["nearest_plant_y"] = np.nan
        eating_herbivores["nearest_neighbour_distance"] = np.nan
        eating_herbivores["nearest_neighbour_index"] = np.nan
        eating_herbivores["nearest_neighbour_size"] = np.nan
        eating_herbivores["target"] = False

        hungry_herbivores = self.select_target(hungry_herbivores)
        if self.herbivore_population.shape[0] > 0 and hungry_herbivores.empty and eating_herbivores.empty:
            pass
        else:
            self.herbivore_population = pd.concat(
                [hungry_herbivores, eating_herbivores]
            ).reset_index(drop=True)
            self._logger.info(f" herbivore_population 1 {self.herbivore_population[['nearest_neighbour_distance', 'nearest_plant_x', 'nearest_plant_y']]}")


    def age(self):
        self.herbivore_population["age"] = self.herbivore_population["age"] + 1
        #TODO Need to think about this. This is a hack because 1/<1 is a big number
        self.herbivore_population["speed"][self.herbivore_population["speed"] < 1] = 1
        self.herbivore_population["perception"][self.herbivore_population["perception"] < 1] = 1
        self.herbivore_population["size"][self.herbivore_population["size"] < 1] = 1

        self.herbivore_population["energy"] = (
            self.herbivore_population["energy"]
            - (1 - (1 / self.herbivore_population["speed"]))
            - (1 - (1 / self.herbivore_population["perception"]))
            + (1 - (1 / self.herbivore_population["size"]))
        )
        self._logger.info((1 - (1 / self.herbivore_population["speed"])) - (1 - (1 / self.herbivore_population["perception"])) + (1 - (1 / self.herbivore_population["size"])))
        self._logger.info(self.herbivore_population[["energy", "speed", "perception", "size"]])

        self.reproduce()
        self.kill_old()
        self.starve()

    def kill_old(self):
        self.herbivore_population = self.herbivore_population.query(
            "age < life_expectancy"
        )

    def starve(self):
        self.herbivore_population = self.herbivore_population.loc[
            self.herbivore_population["energy"] > 0
        ]

    def reproduce(self):
        reproducing_individuals = self.herbivore_population.query(
            "energy > reproduction_energy"
        )
        self._logger.info(reproducing_individuals[['energy', 'reproduction_energy']])
        babies = reproducing_individuals.copy()
        non_repoducing_individuals = self.herbivore_population.loc[
            ~self.herbivore_population.index.isin(reproducing_individuals.index)
        ]
        babies["x"] = babies["x"] + random.uniform(-15, 15)
        babies["y"] = babies["y"] + random.uniform(-15, 15)
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
        babies["size"] = babies["size"] + random.uniform(
            -self.herbivore_properties["mutation_rate"],
            self.herbivore_properties["mutation_rate"],
        )
        babies["perception"] = babies["perception"] + random.uniform(
            -self.herbivore_properties["mutation_rate"],
            self.herbivore_properties["mutation_rate"],
        )
        babies["perception_radius"] = babies["perception"] * 10
        babies["max_movesize"] = (
            (np.power(babies["speed"], 3)) - (np.power(babies["size"], 2))
        ) / self.herbivore_properties["movesize"]
        babies["nearest_plant_x"] = np.nan
        babies["nearest_plant_y"] = np.nan
        babies["nearest_neighbour_distance"] = np.nan
        babies["nearest_neighbour_index"] = np.nan
        babies["nearest_neighbour_size"] = np.nan
        babies["target"] = False
        babies["energy"] = self.herbivore_properties['starting_energy']
        babies["age"] = 0
        self._logger.info(babies[['energy', 'reproduction_energy']])
        reproducing_individuals["energy"] = self.herbivore_properties['starting_energy']
        self.herbivore_population = pd.concat(
            [babies, reproducing_individuals, non_repoducing_individuals]
        ).reset_index(drop=True)
