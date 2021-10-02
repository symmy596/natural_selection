import logging
import random
from src.environment.environment import Environment
from src.organism.carnivore import Carnivore
from src.organism.herbivore import Herbivore
from src.plant.plant import Plant
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
from src.simulation.helpers import nearest_nieghbour


class Simulation:
    name = "simulation"
    plants = Plant
    herbivores = Herbivore
    historic_plants = []
    historic_plant_reproduction_rate = []
    historic_herbivores = []
    historic_steps = []
    line = plt.scatter
    fig = plt.figure
    ax = plt.subplots

    def __init__(self,
                 nplants,
                 nherbivores,
                 ncarnivores,
                 envsize,
                 steps):

        self._nplants = nplants
        self._nherbivores = nherbivores
        self._ncarnivores = ncarnivores
        self._envsize = envsize
        self._steps = steps
        self._logger = logging.getLogger(__name__)
        self._logger.info(f"Initiating {self.name}")

    def setup_simulation(self):
        self.plants = Plant(nplants=self._nplants, envsize=self._envsize)
        self.herbivores = Herbivore(nherbivores=self._nherbivores, envsize=self._envsize)
        #Setup Herbivore locations / Properties
        #Setup Carnivore locations / Properties

    def herbivore_plant_interaction(self):
        herbivore_index, plant_index, plant_sizes = nearest_nieghbour(self.plants.plant_population, self.herbivores.herbivore_population)
        self.herbivores.eat(herbivore_index, plant_sizes)
        self.plants.die(plant_index)

    def sample(self):
        self.historic_plants.append(self.plants.plant_population.shape[0])
        self.historic_plant_reproduction_rate.append(np.mean(self.plants.plant_population.reproduction_rate))
        self.historic_herbivores.append(self.herbivores.herbivore_population.shape[0])

    def setup_animation(self):
        fig = plt.gcf()
        fig.show()
        fig.canvas.draw()

        ax1 = plt.subplot(2,2,1)
        ax1.plot([0], [0], ls='-', color='green')
        ax1.plot([0], [0], ls='-', color='blue')

        ax2 = plt.subplot(2,2,2)
        ax2.plot([0], [0], ls='-', color='red')
        ax2.set_ylim(0.6, 0.61)

        ax3 = plt.subplot(2,2,3)
        ax3.scatter(self.herbivores.herbivore_population.x, self.herbivores.herbivore_population.y, color='blue')
        ax3.set_ylim(0, self._envsize)
        ax3.set_xlim(0, self._envsize)

        plt.pause(0.001)
        fig.canvas.draw()
        return fig, ax1, ax2, ax3

    def update_animation(self, fig, ax1, ax2, ax3):
        ax1.plot(self.historic_steps, self.historic_plants, ls='-', color='green')
        ax1.plot(self.historic_steps, self.historic_herbivores, ls='-', color='blue')
        ax2.plot(self.historic_steps, self.historic_plant_reproduction_rate, ls='-', color='green')
        ax3.clear()
        ax3.scatter(self.herbivores.herbivore_population.x, self.herbivores.herbivore_population.y, color='blue')
        plt.pause(0.001)
        fig.canvas.draw()
        return fig, ax1, ax2, ax3

    def run(self):
        self.setup_simulation()
        fig, ax1, ax2, ax3 = self.setup_animation()
        self._logger.info("Starting simulation")
        for i in range(self._steps):
            self.historic_steps.append(i)

            self.herbivores.move()
            self.herbivore_plant_interaction()
            self.herbivores.age()

            self.plants.grow_plants()

            self.sample()
            fig, ax1, ax2, ax3 = self.update_animation(fig, ax1, ax2, ax3)
