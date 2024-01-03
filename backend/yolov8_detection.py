from utils.config_yaml import ConfigManager
from helpers.detector import ObjectDetectionHelper

config_manager = ConfigManager()
config = config_manager.get_config()
model_config = config.get('object_config')


def get_model(weights):
    model_config['weights_path'] = weights
    detector = ObjectDetectionHelper(model_config)
    return detector
