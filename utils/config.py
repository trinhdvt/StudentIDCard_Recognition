ROOT_CONTENT = "/home/dvt/Desktop/StudentIDCard_Recognition"
DETECTOR_CFG = f"{ROOT_CONTENT}/detector/config/detector_model.cfg"

DETECTOR_WEIGHT = f"{ROOT_CONTENT}/detector/config/detector_model.weights"
# DETECTOR_WEIGHT_DRIVE_ID = "1--xguD0tT37zG7P5mGoNaUBTp3RUgMqz"

READER_CFG = f"{ROOT_CONTENT}/reader/config/cfg.yml"
READER_WEIGHT = f"{ROOT_CONTENT}/reader/config/transformerocr.pth"
BACKUP_READER_WEIGHT = f"{ROOT_CONTENT}/reader/config/transformerocr2.pth"
DEVICE = "cpu"
API_NAME = "/id_recognize"
API_ADDRESS = "0.0.0.0"
API_PORT = "8000"
API_URL = f"http://{API_ADDRESS}:{API_PORT}{API_NAME}"
IMG_WIDTH = 768
IMG_HEIGHT = 480
