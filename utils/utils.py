import cv2
import numpy as np
import base64


def cv2img_to_base64(cv2_img=None, img_path=None):
    assert cv2_img is not None or img_path is not None
    if cv2_img:
        _, im_arr = cv2.imencode(".jpg", cv2_img)
        im_bytes = im_arr.tobytes()
    elif img_path:
        with open(img_path, "rb") as f:
            im_bytes = f.read()

    return base64.b64encode(im_bytes)


def base64_to_cv2img(b64_encoded: str):
    assert b64_encoded is not None
    b64_decoded = base64.b64decode(b64_encoded)
    img = np.frombuffer(b64_decoded, dtype=np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    return img
