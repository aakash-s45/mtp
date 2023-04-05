import yaml
import argparse

# Define the command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--config', required=True, help='Path to the config YAML file')

# Parse the arguments
args = parser.parse_args()

# Load the YAML file
with open(args.config, 'r') as f:
    config = yaml.safe_load(f)

    filePath = config['filePath']
    tileSize = int(config['tileSize'])
    SPLIT_DATA = bool(config['SPLIT_DATA'])
    alpha = float(config['alpha'])
    slope = float(config['slope'])
    h_weight = float(config['h_weight'])
    DEBUG = bool(config['DEBUG'])
    SHOW_PLOT = bool(config['SHOW_PLOT'])
    # print(filePath)

    