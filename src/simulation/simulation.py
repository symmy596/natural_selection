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
    historic_plant_offspring_spread = []
    historic_herbivores = []
    historic_herbivores_size = []
    historic_herbivores_speed = []
    historic_herbivores_perception = []
    historic_herbivores_energy = []
    historic_steps = []
    line = plt.scatter
    fig = plt.figure
    ax = plt.subplots

    def __init__(self, simulation_parameters):

        self._plant_properties = simulation_parameters["plant_properties"]
        self._herbivores_properties = simulation_parameters["herbivore_properties"]
        self._ncarnivores = simulation_parameters["carnivores_properties"]
        self._envsize = simulation_parameters["size"]
        self._steps = simulation_parameters["steps"]
        self._logger = logging.getLogger(__name__)
        self._logger.info(f"Initiating {self.name}")

    def setup_simulation(self):
        self.plants = Plant(
            plant_properties=self._plant_properties, envsize=self._envsize
        )
        self.herbivores = Herbivore(
            herbivore_properties=self._herbivores_properties, envsize=self._envsize
        )

    def herbivore_plant_interaction(self):
        self.herbivores.herbivore_population = nearest_nieghbour(
            self.plants.plant_population, self.herbivores.herbivore_population
        )

        self.plants.die(self.herbivores.herbivore_population)

        self.herbivores.eat()


    def sample(self):
        self.historic_plants.append(self.plants.plant_population.shape[0])
        self.historic_plant_reproduction_rate.append(
            np.mean(self.plants.plant_population.reproduction_rate)
        )
        self.historic_plant_size.append(np.mean(self.plants.plant_population["size"]))
        self.historic_plant_offspring_spread.append(np.mean(self.plants.plant_population['offspring_spread']))
        self.historic_herbivores.append(self.herbivores.herbivore_population.shape[0])
        self.historic_herbivores_perception.append(
            np.mean(self.herbivores.herbivore_population["perception"])
        )
        self.historic_herbivores_speed.append(
            np.mean(self.herbivores.herbivore_population["speed"])
        )
        self.historic_herbivores_size.append(
            np.mean(self.herbivores.herbivore_population["size"])
        )
        self.historic_herbivores_energy.append(
            np.mean(self.herbivores.herbivore_population["energy"])
        )

    def setup_animation(self):
        fig = plt.gcf()
        fig.show()
        fig.canvas.draw()
        fig.set_size_inches(8, 8)
        ax1 = plt.subplot(2, 3, 1)
        ax1.plot([0], [0], ls="-", color="green")
        ax1.plot([0], [0], ls="-", color="blue")
        # ax1.set_xlim(50, self._steps)
        ax2 = plt.subplot(2, 3, 2)
        ax2.plot([0], [0], ls="-", color="red")
        ax2.plot([0], [0], ls="-", color="green")
        # ax2.set_ylim(0.6, 0.61)

        ax3 = plt.subplot(2, 3, 3)
        ax3.scatter(
            self.herbivores.herbivore_population.x,
            self.herbivores.herbivore_population.y,
            color="blue",
        )
        ax3.set_ylim(0, self._envsize)
        ax3.set_xlim(0, self._envsize)

        ax4 = plt.subplot(2, 3, 4)
        ax4.plot([0], [0])
        ax4.plot([0], [0])
        ax4.plot([0], [0])

        ax5 = plt.subplot(2, 3, 5)
        ax5.plot([0], [0])

        plt.pause(0.001)
        fig.canvas.draw()
        return fig, ax1, ax2, ax3, ax4, ax5

    def update_animation(self, fig, ax1, ax2, ax3, ax4, ax5):
        ax1.clear()
        ax2.clear()
        ax3.clear()
        ax4.clear()
        ax5.clear()

        ax1.plot(
            self.historic_steps,
            self.historic_plants,
            ls="-",
            color="green",
            label="plants",
        )
        ax1.plot(
            self.historic_steps,
            self.historic_herbivores,
            ls="-",
            color="blue",
            label="herbivores",
        )
        ax1.legend()
        # ax1.set_xlim(50, self._steps)

        ax2.plot(
            self.historic_steps,
            self.historic_plant_reproduction_rate,
            ls="-",
            color="red",
            label="reproduction rate",
        )
        ax2.plot(
            self.historic_steps,
            self.historic_plant_size,
            ls="-",
            color="green",
            label="size",
        )
        ax2.plot(
            self.historic_steps,
            self.historic_plant_offspring_spread,
            ls="-",
            color="blue",
            label="spread",
        )
        ax2.legend()
        ax3.scatter(
            self.herbivores.herbivore_population.x,
            self.herbivores.herbivore_population.y,
            color="blue",
            s=10,
        )
        ax3.scatter(
            self.plants.plant_population.x,
            self.plants.plant_population.y,
            color="green",
            s=5,
        )

       # ax3.set_ylim(0, self._envsize)
       # ax3.set_xlim(0, self._envsize)
        ax4.plot(
            self.historic_steps,
            self.historic_herbivores_size,
            color="red",
            label="Size",
        )
        ax4.plot(
            self.historic_steps,
            self.historic_herbivores_speed,
            color="blue",
            label="Speed",
        )
        ax4.plot(
            self.historic_steps,
            self.historic_herbivores_perception,
            color="green",
            label="Perception",
        )
        ax4.legend()
        ax5 = plt.subplot(2, 3, 5)
        ax5.plot(self.historic_steps, self.historic_herbivores_energy)
        plt.pause(0.001)
        fig.canvas.draw()
        return fig, ax1, ax2, ax3, ax4, ax5

    def run(self):
        self.setup_simulation()

        fig, ax1, ax2, ax3, ax4, ax5 = self.setup_animation()
        self._logger.info("Starting simulation")
        for i in range(self._steps):
            if self.herbivores.herbivore_population.shape[0] == 0:
                self._logger.info("Herbivores have stared to death")
                break
            elif self.plants.plant_population.shape[0] == 0:
                self._logger.info(
                    "Plants have gone extinct. Ecological collapse incoming"
                )
                self.historic_steps.append(i)
                self.herbivores.move()
                self.herbivores.age()
                self.sample()
                fig, ax1, ax2, ax3, ax4, ax5 = self.update_animation(fig, ax1, ax2, ax3, ax4, ax5)
            else:
                self.historic_steps.append(i)

                self.herbivore_plant_interaction()
                self.herbivores.move()

                self.herbivores.age()

                self.plants.grow_plants()

                self.sample()
                fig, ax1, ax2, ax3, ax4, ax5 = self.update_animation(fig, ax1, ax2, ax3, ax4, ax5)
        plt.savefig("end_pane.png")
        time.sleep(10000)
