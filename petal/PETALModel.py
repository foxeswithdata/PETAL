from petal.patch_runner import PatchRunner


class PETALModel():
    """PETAL parent class
    Determine if running single patch or multipatch run. Then store either single patch or patch list.
    Control the passing of environmental/abiotic values to each patch/

    Args:
        config: Filepath of the YAML-configuration file
    """

    def __init__(self, config):
        print("Initializing PETAL model")

        self.config = config

        # Need direct mapping between indices of patch and climate
        self.patch = []
        self.climate = []

        if config['general']['multipatch']:
            print("Multipatch behaviour not yet supported")

        else:
            print("initialising single patch")
            self.patch = PatchRunner(config)

