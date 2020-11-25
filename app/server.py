from utils.utils import base64_to_cv2img
from utils.utils import cv2img_to_base64
from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
from PIL import Image
from utils.utils import load_model
from utils import config
import time

global cropper
global detector
global reader

app = Flask(__name__)
CORS(app)


@app.route("/")
@cross_origin()
def index():
    return "Welcome to Flask API"


@app.route(config.MSSV_API_NAME, methods=['POST'])
@cross_origin()
def run_for_your_life():
    start = time.time()
    # get data from request
    img_b64 = request.form.get('image')
    # convert base64 string to img
    img = base64_to_cv2img(img_b64)
    # run module id recognize
    cropped = cropper.predict(img, resize=False)
    try:
        id_only_img, _ = detector.predict(cropped)
    except TypeError:
        return "Failed!"
    try:
        assert id_only_img is not None
        id_only_img = Image.fromarray(id_only_img)
        mssv = reader.predict(id_only_img)
        end = time.time()
        # send back data
        return_data = {
            'mssv': mssv,
            'time': end - start,
            'image': cv2img_to_base64(None, cropped, False).decode('utf-8')
        }
        return return_data
    except AssertionError:
        return "Failed!"


if __name__ == '__main__':
    print("Model is loading")
    cropper, detector, reader = load_model()
    print("Model is ready!")
    app.run(debug=True, host=config.MSSV_API_ADDRESS, port=config.API_PORT)
