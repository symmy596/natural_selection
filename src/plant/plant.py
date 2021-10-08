import logging
import random
import pandas as pd
import numpy as np


class Plant:
    name = "plant"
    plant_population = pd.DataFrame
    sign_multiplier = [-1, 1]

    def __init__(self, plant_properties, envsize):
        self.plant_properties = plant_properties
        self.envsize = envsize
        # TODO These need to be set in simulation parameters
        x = np.random.uniform(0, self.envsize, self.plant_properties["starting_number"])
        y = np.random.uniform(0, self.envsize, self.plant_properties["starting_number"])
        size = np.random.uniform(
            self.plant_properties["size"][0],
            self.plant_properties["size"][1],
            self.plant_properties["starting_number"],
        )
        reproduction_rate = np.random.uniform(
            self.plant_properties["reproduction_rate"][0],
            self.plant_properties["reproduction_rate"][1],
            self.plant_properties["starting_number"],
        )
        offspring_spread = np.random.uniform(
            self.plant_properties["offspring_spread"][0],
            self.plant_properties["offspring_spread"][1],
            self.plant_properties["starting_number"],
        )
        offspring_spread_size = np.power(offspring_spread, 3) + np.power(size, 2)
        self.plant_population = pd.DataFrame(
            {
                "x": x,
                "y": y,
                "size": size,
                "reproduction_rate": reproduction_rate,
                "offspring_spread": offspring_spread,
                "offspring_spread_size": offspring_spread_size,
            }
        )
        self.plant_population["env_size"] = 1000
        self._logger = logging.getLogger(__name__)
        self._logger.debug(f"Initiating {self.name}")

    def grow_plants(self):
        self.plant_population["random_chance"] = np.random.uniform(
            0, 1, self.plant_population.shape[0]
        )
        self.plant_population["reproduction_chance"] = (
            self.plant_population["reproduction_rate"]
            + self.plant_population["random_chance"]
            - (self.plant_population["size"] / 2)
        )
        reproducing_plants = self.plant_population.nlargest(
            self.plant_properties["replication_percentage"], "reproduction_chance"
        )
        reproducing_plants["x"] = reproducing_plants["x"] + np.copysign(
            reproducing_plants["offspring_spread_size"],(
                    self.envsize
                    - (
                        reproducing_plants["x"]
                        + reproducing_plants["offspring_spread_size"]
                    )
            ),
        )
        reproducing_plants["y"] = reproducing_plants["y"] + np.copysign(
            reproducing_plants["offspring_spread_size"],
                (
                    self.envsize
                    - (
                        reproducing_plants["y"]
                        + reproducing_plants["offspring_spread_size"]
                    )
            ),
        )
        reproducing_plants.x[reproducing_plants.x > self.envsize] = np.random.uniform(
            0, self.envsize, reproducing_plants.shape[0]
        )
        reproducing_plants.y[reproducing_plants.y > self.envsize] = np.random.uniform(
            0, self.envsize, reproducing_plants.shape[0]
        )
        reproducing_plants.x[reproducing_plants.x < self.envsize] = np.random.uniform(
            0, self.envsize, reproducing_plants.shape[0]
        )
        reproducing_plants.y[reproducing_plants.y < self.envsize] = np.random.uniform(
            0, self.envsize, reproducing_plants.shape[0]
        )
        reproducing_plants["size"] = reproducing_plants["size"] + random.uniform(
            -self.plant_properties["mutation_rate"],
            self.plant_properties["mutation_rate"],
        )
        reproducing_plants["reproduction_rate"] = reproducing_plants[
            "reproduction_rate"
        ] + random.uniform(
            -self.plant_properties["mutation_rate"],
            self.plant_properties["mutation_rate"],
        )
        reproducing_plants["offspring_spread"] = reproducing_plants[
            "offspring_spread"
        ] + random.uniform(
            -self.plant_properties["mutation_rate"],
            self.plant_properties["mutation_rate"],
        )
        reproducing_plants["offspring_spread_size"] = np.power(
            reproducing_plants["offspring_spread"], 3
        ) + np.power(reproducing_plants["size"], 2)
        self.plant_population = pd.concat(
            [self.plant_population, reproducing_plants]
        ).reset_index(drop=True)
        self.plant_population.drop(columns=["reproduction_chance", "random_chance"])
        self.nplants = self.plant_population.shape[0]

    def die(self, distances):
        eaten_plants = distances.loc[distances["nearest_neighbour_distance"] < 10.0]
        self.plant_population = self.plant_population.loc[
            ~self.plant_population.index.isin(eaten_plants["nearest_neighbour_index"])
        ]
