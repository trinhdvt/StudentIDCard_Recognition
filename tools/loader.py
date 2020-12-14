from cropper.Cropper import Cropper
from detector.Detector import Detector
from reader.Reader import Reader
from reader.Config import Cfg
from tools import config


def load_model():
    cropper = Cropper()
    detector = Detector(config.DETECTOR_CFG, config.DETECTOR_WEIGHT)
    reader_config = Cfg.load_config_from_file(config.READER_CFG)
    reader_config['weights'] = config.READER_WEIGHT
    reader_config['device'] = config.DEVICE
    reader = Reader(reader_config)
    return cropper, detector, reader
