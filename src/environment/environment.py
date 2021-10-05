import logging
import numpy as np


class Environment:
    name = "environment"

    def __init__(self, size):
        self._size = size
        self._logger = logging.getLogger(__name__)
        self._logger.info(f"Initiating {self.name}")

    @property
    def world(self):
        return np.zeros(shape=(self._size, self._size))
