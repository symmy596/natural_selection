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


def main(simulation_parameters):

    simulation = Simulation(simulation_parameters)
    simulation.run()


with open('src/simulation_parameters.json') as file:
    simulation_parameters = json.load(file)

logger.info(
    f"""Received input variables:
            Starting plants: {simulation_parameters['plant_properties']['starting_number']}
            Starting herbivores: {simulation_parameters['herbivore_properties']['starting_number']}
            Starting carnivores: {simulation_parameters['carnivores_properties']['starting_number']}
            Size: {simulation_parameters['size']}
            Steps: {simulation_parameters['steps']}
        """
)

main(simulation_parameters)