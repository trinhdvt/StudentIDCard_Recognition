from utils.utils import cv2img_to_base64
from utils import config
import requests


def send_request(url, img_path):
    im_b64 = cv2img_to_base64(img_path)
    params = {
        'image': im_b64
    }
    response = requests.post(url, data=params)
    return response.text


if __name__ == '__main__':
    local_img = "./test/dung4.jpg"
    print(send_request(config.API_URL, local_img))
    local_img = "./test/hai2.jpg"
    print(send_request(config.API_URL, local_img))
