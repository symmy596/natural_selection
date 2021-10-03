import logging
from src.organism.herbivore import Herbivore
from src.plant.plant import Plant
import matplotlib.pyplot as plt
import numpy as np
from src.simulation.helpers import nearest_nieghbour
import time


class Simulation:
    name = "simulation"
    plants = Plant
    herbivores = Herbivore
    historic_plants = []
    historic_plant_reproduction_rate = []
    historic_plant_size = []
    historic_herbivores = []
    historic_herbivore_energy = []
    historic_herbivores_life_expectancy = []
    historic_herbivores_reproduction_energy = []
    historic_herbivores_speed = []
    historic_steps = []

    line = plt.scatter
    fig = plt.figure
    ax = plt.subplots

    def __init__(self, simulation_parameters):

        self._nplants = simulation_parameters['plant properties']['starting number']
        self._plants_replication_rate = simulation_parameters['plant properties']['replication percentage']
        self._plants_replication_method = simulation_parameters['plant properties']['replication method']
        self._nherbivores = simulation_parameters['herbivore properties']['starting number']
        self._ncarnivores = simulation_parameters['carnivores properties']['starting number']
        self._envsize = simulation_parameters['size']
        self._steps = simulation_parameters['steps']
        self._logger = logging.getLogger(__name__)
        self._logger.info(f"Initiating {self.name}")

    def setup_simulation(self):
        self.plants = Plant(nplants=self._nplants,
                            replication_rate=self._plants_replication_rate,
                            replication_method=self._plants_replication_method,
                            envsize=self._envsize)
        self.herbivores = Herbivore(nherbivores=self._nherbivores, envsize=self._envsize)

    def herbivore_plant_interaction(self):
        nn_df = nearest_nieghbour(self.plants.plant_population, self.herbivores.herbivore_population)
        self.herbivores.eat(nn_df)
        self.plants.die(nn_df)

    def sample(self):
        self.historic_plants.append(self.plants.plant_population.shape[0])
        self.historic_plant_reproduction_rate.append(np.mean(self.plants.plant_population.reproduction_rate))
        self.historic_plant_size.append(np.mean(self.plants.plant_population['size']))
        self.historic_herbivores.append(self.herbivores.herbivore_population.shape[0])
        self.historic_herbivore_energy.append(np.mean(self.herbivores.herbivore_population.energy))
        self.historic_herbivores_speed.append(np.mean(self.herbivores.herbivore_population.speed))
        self.historic_herbivores_life_expectancy.append(np.mean(self.herbivores.herbivore_population.life_expectancy))
        self.historic_herbivores_reproduction_energy.append(np.mean(self.herbivores.herbivore_population.reproduction_energy))

    def setup_animation(self):
        fig = plt.gcf()
        fig.show()
        fig.canvas.draw()
        fig.set_size_inches(8, 8)
        ax1 = plt.subplot(2,2,1)
        ax1.plot([0], [0], ls='-', color='green')
        ax1.plot([0], [0], ls='-', color='blue')
        #ax1.set_xlim(50, self._steps)
        ax2 = plt.subplot(2,2,2)
        ax2.plot([0], [0], ls='-', color='red')
        ax2.plot([0], [0], ls='-', color='green')
        #ax2.set_ylim(0.6, 0.61)

        ax3 = plt.subplot(2,2,3)
        ax3.scatter(self.herbivores.herbivore_population.x, self.herbivores.herbivore_population.y, color='blue')
        ax3.set_ylim(0, self._envsize)
        ax3.set_xlim(0, self._envsize)

        ax4 = plt.subplot(2,2,4)
        ax4.plot([0], [0])
     #   ax4.plot([0], [0])
        ax4.plot([0], [0])
        ax4.plot([0], [0])
        plt.pause(0.001)
        fig.canvas.draw()
        return fig, ax1, ax2, ax3, ax4

    def update_animation(self, fig, ax1, ax2, ax3, ax4):
        ax1.clear()
        ax2.clear()
        ax3.clear()
        ax4.clear()

        ax1.plot(self.historic_steps, self.historic_plants, ls='-', color='green', label='plants')
        ax1.plot(self.historic_steps, self.historic_herbivores, ls='-', color='blue', label='herbivores')
        ax1.legend()
        #ax1.set_xlim(50, self._steps)

        ax2.plot(self.historic_steps, self.historic_plant_reproduction_rate, ls='-', color='red', label='reproduction rate')
        ax2.plot(self.historic_steps, self.historic_plant_size, ls='-', color='green', label='size')
        ax2.legend()
        #ax3.scatter(self.herbivores.herbivore_population.x, self.herbivores.herbivore_population.y, color='blue')
        ax3.hist2d(self.plants.plant_population.x, self.plants.plant_population.y, bins=(50, 50), cmap='viridis')
        ax3.set_ylim(0, self._envsize)
        ax3.set_xlim(0, self._envsize)
        ax4.plot(self.historic_steps, self.historic_herbivore_energy, color='red', label='energy')
        ax4.plot(self.historic_steps, self.historic_herbivores_speed, color='blue', label='speed')
        ax4.plot(self.historic_steps, self.historic_herbivores_reproduction_energy, color='green', label='reproduction energy')
        ax4.legend()
        #ax4.plot(self.historic_steps, self.historic_herbivores_life_expectancy, color='black')

        plt.pause(0.001)
        fig.canvas.draw()
        return fig, ax1, ax2, ax3, ax4

    def run(self):
        self.setup_simulation()

        fig, ax1, ax2, ax3, ax4 = self.setup_animation()
        self._logger.info("Starting simulation")
        for i in range(self._steps):
            self.historic_steps.append(i)

            self.herbivore_plant_interaction()

            self.herbivores.move()

            self.herbivores.age()

            self.plants.grow_plants()
            #self._logger.info(f"Plants {self.plants.plant_population}")
            #self._logger.info(f"Hervivores {self.herbivores.herbivore_population}")
            self.sample()
            fig, ax1, ax2, ax3, ax4 = self.update_animation(fig, ax1, ax2, ax3, ax4)
        plt.savefig("end_pane.png")
        time.sleep(10000)