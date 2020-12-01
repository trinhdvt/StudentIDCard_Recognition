from datetime import datetime
from utils import config
from PIL import Image
import cv2
import numpy as np
import base64
import os
import gdown


def resize_img(img, img_path=None):
    if img_path:
        img = cv2.imread(img_path)
    (h, w, _) = img.shape
    if w > config.IMG_WIDTH:
        ratio = config.IMG_WIDTH / float(w)
        dim = (config.IMG_WIDTH, int(ratio * h))
        img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return img


def cv2img_to_pil(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return Image.fromarray(img)


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


def download_model(model_name):
    url = "https://drive.google.com/uc?id="
    if model_name == "detector":
        gdown.download(url + config.DETECTOR_WEIGHT_DRIVE_ID,
                       config.DETECTOR_WEIGHT)
    elif model_name == "reader":
        gdown.download(url + config.READER_WEIGHT_DRIVE_ID,
                       config.READER_WEIGHT)
    elif model_name == "reader_backup":
        gdown.download(url + config.READER_BACKUP_WEIGHT_DRIVE_ID,
                       config.READER_BACKUP_WEIGHT)
    else:
        raise Exception("Unknown model!")


def parse_img_size(cfg_path):
    """

    :param cfg_path: Config path for detector (YOLOv4's config file only)
    :return: img_width and img_height in config file
    """
    img_width = None
    img_height = None
    with open(cfg_path, "r") as f:
        while f.readable():
            line = f.readline()
            if line.startswith("width"):
                img_width = int(line.split('=')[-1])
            if line.startswith("height"):
                img_height = int(line.split('=')[-1])
            if img_height and img_height:
                return img_width, img_height
    assert img_width is not None
    assert img_height is not None
