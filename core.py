import json
import logging
import os
import sys

from src.simulation.simulation import Simulation


def setup_logging():
    logger = logging.getLogger()
    for h in logger.handlers:
        logger.removeHandler(h)

    ch = logging.StreamHandler(sys.stdout)

    console_formatter = logging.Formatter(
        "%(asctime)s.%(msecs)3d-%(name)-18s: %(levelname)-8s %(message)s"
    )
    ch.setFormatter(console_formatter)
    logger.addHandler(ch)
    if os.getenv("LOGFILE"):
        file_formatter = logging.Formatter(
            "%(asctime)s.%(msecs)d::%(name)s::%(levelname)s::%(message)s"
        )
        fh = logging.FileHandler(filename=os.getenv("LOGFILE", "src/core.log"))
        fh.setFormatter(file_formatter)
        logger.addHandler(fh)
    loglevel = getattr(logging, os.getenv("LOGLEVEL", "INFO").upper())
    logger.setLevel(loglevel)

    return logger

logger = setup_logging()
logger.info(os.getenv("LOGLEVEL", "No LOGLEVEL set, using INFO"))
logger.debug(
    os.getenv("LOGFILE", "No LOGFILE set, it will not create the log file by default")
)


def main(nplants,
         nherbivores,
         ncarnivores,
         envsize,
         steps):

    simulation = Simulation(nplants=nplants,
                            nherbivores=nherbivores,
                            ncarnivores=ncarnivores,
                            envsize=envsize,
                            steps=steps
                            )
    simulation.run()


with open('src/simulation_parameters.json') as file:
    simulation_parameters = json.load(file)

nplants = simulation_parameters['plants']
nherbivores = simulation_parameters['herbivores']
ncarnivores = simulation_parameters['carnivores']
envsize = simulation_parameters['size']
steps = simulation_parameters['steps']

logger.info(
    f"""Received input variables:
            Plants: {nplants}
            Herbivores: {nherbivores}
            Carnivores: {ncarnivores}
            Size: {envsize}
            Steps: {steps}
        """
)

main(
    nplants=nplants,
    nherbivores=nherbivores,
    ncarnivores=ncarnivores,
    envsize=envsize,
    steps=steps,
)