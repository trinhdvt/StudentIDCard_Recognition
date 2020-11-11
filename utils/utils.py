from cropper.Cropper import Cropper
from detector.Detector import Detector
from reader.Reader import Reader
from reader.Config import Cfg
from utils import config as cfg
import cv2
import numpy as np
import base64


def load_model():
    cropper = Cropper()
    detector = Detector(cfg.DETECTOR_CFG, cfg.DETECTOR_WEIGHT)
    reader_cfg = Cfg.load_config_from_file(cfg.READER_CFG)
    reader_cfg['weights'] = cfg.READER_WEIGHT
    reader_cfg['device'] = cfg.DEVICE
    reader = Reader(reader_cfg)
    return cropper, detector, reader


def resize_img(img):
    (h, w, _) = img.shape
    if (w, h) > (cfg.IMG_WIDTH, cfg.IMG_HEIGHT):
        if w > h:
            img = cv2.resize(img, (cfg.IMG_WIDTH, cfg.IMG_HEIGHT))
        else:
            img = cv2.resize(img, (cfg.IMG_HEIGHT, cfg.IMG_WIDTH))
    return img


def cv2img_to_base64(img_path: str):
    img = cv2.imread(img_path)
    cv2_img = resize_img(img)
    _, im_arr = cv2.imencode(".jpg", cv2_img)
    im_bytes = im_arr.tobytes()

    return base64.b64encode(im_bytes)


def base64_to_cv2img(b64_encoded: str):
    assert b64_encoded is not None
    b64_decoded = base64.b64decode(b64_encoded)
    img = np.frombuffer(b64_decoded, dtype=np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    return img
