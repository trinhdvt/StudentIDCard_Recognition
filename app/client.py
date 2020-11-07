from utils.utils import cv2img_to_base64
import requests
import time

start = time.time()
url = 'http://127.0.0.1:8000/id_recognize'
img_path = "../cropper/test_img/tung2.jpg"
im_b64 = cv2img_to_base64(cv2_img=None, img_path=img_path)
results = requests.post(url, data={
    'image': im_b64
})
print(time.time() - start)
print(results)
print(results.text)
