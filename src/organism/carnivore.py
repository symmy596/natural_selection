import logging


class Carnivore:
    type = "carnivore"

    def __init__(self, environment):
        self._environment = environment
        self._logger = logging.getLogger(__name__)
        super().__init__(type=self.type, logger=self._logger)
