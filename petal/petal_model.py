from petal.patch_runner import PatchRunner
from petal.reporter import Reporter
from petal.climate import Climate
import logging

import pandas as pd
from datetime import timedelta




class PETALModel():
    """PETAL parent class
    Determine if running single patch or multipatch run. Then store either single patch or patch list.
    Control the passing of environmental/abiotic values to each patch/

    Args:
        config: Filepath of the YAML-configuration file
    """

    def __init__(self, config):
        log = logging.getLogger(__name__)
        log.debug("Initializing PETAL model \n")

        self.config = config

        self.start_date = pd.Timestamp(config["general"]["start_date"])
        self.end_date = pd.Timestamp(config["general"]["end_date"])
        # Need direct mapping between indices of patch and climate
        self.patch = []
        self.climate = []

        if 'report' not in config:
            raise KeyError(f"Missing 'report' section in config. Found: {list(config)}")
        self.reporter = Reporter(config['report'])

        if config['general']['multipatch']:
            log.debug("Initialising Multiple Patch")
            log.error("Multipatch behaviour not yet supported")
            raise NotImplementedError("Multipatch behaviour not yet supported")

        else:
            log.debug("Initialising Single Patch")
            self.patch = PatchRunner(config)
            self.climate = Climate(config)

    def run_test(self):
        log = logging.getLogger(__name__)
        log.debug("Running test \n")

        self.climate.print()

        for self.current_time in pd.date_range(self.start_date, self.end_date, freq="D"):
            log.debug(f"Running step {self.current_time}")

            self.patch.calculateRates(self.climate.temperature.loc[self.current_time])
            self.patch.step(None)

            print("\n\n")



