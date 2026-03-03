# importing required modules
import argparse
import yaml

from petal.PETALModel import PETALModel

# create a parser object
parser = argparse.ArgumentParser(description = "PETAL - Pollinator Model")

default_config = "model.yml"

# add argument
parser.add_argument("-c", "--config", nargs = 1, metavar = "filename", type = str,
                     help = f"Path of the model configuration file. Defaults to '{default_config}'.")
parser.add_argument('-v', '--verbose',
                    action='store_true')

# parse the arguments from standard input
args = parser.parse_args()

### Load configuration file
config_path = args.config

if config_path is None:
    config_path = default_config
else:
    config_path = config_path[0]

with open(config_path) as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

PETALModel = PETALModel(config)


