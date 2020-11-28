from cropper.Cropper import Cropper
from detector.Detector import Detector
from reader.Reader import Reader
from reader.Config import Cfg
from utils import config as cfg
from datetime import datetime
from utils import config
import cv2
import numpy as np
import base64
import os


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


def save_to_local(bsx_data: tuple, sv_data: tuple) -> tuple:
    """

    :param bsx_data: (bsx_text, bsx_image)
    :param sv_data:  (mssv_text, mssv_image)
    :return: (bsx_img_path, mssv_img_path)
    """
    bsx_text, bsx_image = bsx_data
    mssv_text, mssv_image = sv_data
    bsx_path, mssv_path = generate_img_path(bsx_text, mssv_text)
    base64_to_cv2img(bsx_image, bsx_path)
    base64_to_cv2img(mssv_image, mssv_path)
    return bsx_path, mssv_path


def generate_img_path(*content):
    """

    :param content: (bsx_text, mssv_text)
    :return: unique path base on current time
    """
    current_time = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    img_paths = [f"{config.LOCAL_IMG_STORAGE}{c}_{current_time}.jpg" for c in content]
    img_paths = [path.replace(" ", "") for path in img_paths]
    return img_paths


def to_web_storage(*img_path):
    for file_path in img_path:
        response_code = os.system(f"scp {file_path} nghiapham@{config.WEB_IP}:{config.WEB_IMG_STORAGE}")
        assert response_code == 0
        os.remove(file_path)

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
