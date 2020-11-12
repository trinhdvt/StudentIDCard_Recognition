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


def resize_img(img, img_path=None):
    if img_path:
        img = cv2.imread(img_path)
    (h, w, _) = img.shape
    if h > cfg.IMG_HEIGHT:
        ratio = cfg.IMG_HEIGHT / float(h)
        dim = (int(ratio * w), cfg.IMG_HEIGHT)
        img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    # if w > cfg.IMG_WIDTH:
    #     ratio = cfg.IMG_WIDTH / float(w)
    #     dim = (cfg.IMG_WIDTH, int(ratio * h))
    #     img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    # if (w, h) > (cfg.IMG_WIDTH, cfg.IMG_HEIGHT):
    #     if w > h:
    #         img = cv2.resize(img, (cfg.IMG_WIDTH, cfg.IMG_HEIGHT))
    #     else:
    #         img = cv2.resize(img, (cfg.IMG_HEIGHT, cfg.IMG_WIDTH))
    return img


def cv2img_to_base64(img_path, img=None, resize=True):
    if img is None:
        img = cv2.imread(img_path)
    if resize:
        img = resize_img(img)
    _, im_arr = cv2.imencode(".jpg", img)
    im_bytes = im_arr.tobytes()

    return base64.b64encode(im_bytes)


def base64_to_cv2img(b64_encoded: str, save_path=None):
    assert b64_encoded is not None
    b64_decoded = base64.b64decode(b64_encoded)
    img = np.frombuffer(b64_decoded, dtype=np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    if not save_path:
        return img
    else:
        cv2.imwrite(save_path, img)
# def resize_ratio(img_path, width):
#     img = cv2.imread(img_path)
#     (h, w, _) = img.shape
#     ratio = width / float(w)
#     dim = (width, int(ratio * h))
#     resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
#     cv2.imwrite("../x.jpg", resized)
#
#
# resize_ratio("../resized_img/hien1.jpg", 768)
