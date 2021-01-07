from cropper.cropper import Cropper
from detector.detector import Detector
from reader.reader import Reader
from reader.config import Cfg
from tools import config


def load_model(backup_reader=False):
    #
    cropper = Cropper()
    #
    detector = Detector(config.DETECTOR_CFG, config.DETECTOR_WEIGHT, config.DETECTOR_LABELS)
    #
    reader_config = Cfg.load_config_from_file(config.READER_CFG)
    reader_config['weights'] = config.READER_WEIGHT
    if backup_reader:
        reader_config['weights'] = config.READER_BACKUP_WEIGHT
    reader_config['device'] = config.DEVICE
    reader = Reader(reader_config, backup_reader)
    #
    return cropper, detector, reader
