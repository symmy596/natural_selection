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

class Simulation:
    name = "simulation"
    plants = Plant
    herbivores = Herbivore
    historic_plants = []
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

    def move_organisms(self):
        pass


    def setup_animation(self):
        fig = plt.gcf()
        fig.show()
        fig.canvas.draw()
        plt.plot([0], [0], ls='-', color='green')
        plt.plot([0], [0], ls='-', color='blue')
        plt.pause(0.01)
        fig.canvas.draw()
        return fig

    def update_animation(self, fig):
        plt.plot(self.historic_steps, self.historic_plants, ls='-', color='green')
        plt.plot(self.historic_steps, self.historic_herbivores, ls='-', color='blue')
        plt.pause(0.01)
        fig.canvas.draw()

    def run(self):
        self.setup_simulation()
        fig = self.setup_animation()
        self._logger.info("Starting simulation")
        for i in range(self._steps):
            self.historic_steps.append(i)
            #Move Herbivores
            #Herbivores Eat food or breed
            self.historic_herbivores.append(self.herbivores.herbivore_population.shape[0])
            self.plants.grow_plants()
            self.historic_plants.append(self.plants.plant_population.shape[0])
            self.update_animation(fig)
