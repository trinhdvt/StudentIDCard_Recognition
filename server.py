import os
import time

import cv2
import numpy as np
from PIL import Image
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin

from tools.loader import load_model
from tools.utils import cv2img_to_base64, cv2img_to_pil

global cropper
global detector
global reader

app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png']
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
app.static_folder = 'static'
CORS(app)


def run_for_my_life2(cv2_img):
    #
    start = time.time()
    origin_img = cv2_img
    #
    try:
        cropped_img = cropper.predict(origin_img, resize=True)
        detect_rs, annotated_img, coordinate = detector.predict(cropped_img, True)
        reader_rs = {}
        #
        cropped_img = cv2img_to_pil(cropped_img)
        for key, value in detect_rs.items():
            text = reader.predict(cv2img_to_pil(value))
            reader_rs[key] = text
    except Exception as e:
        return {'massage': str(e)}, 406
    #
    end = time.time()
    # send back data
    cropped_img = cv2.cvtColor(np.array(cropped_img), cv2.COLOR_RGB2BGR)
    return_data = {
        'time': end - start,
        'image': cv2img_to_base64(None, cropped_img, False).decode('utf-8')
    }
    return_data.update(reader_rs)
    return return_data, 200


@app.route("/", methods=['GET', 'POST'])
@cross_origin()
def index():
    return render_template('index.html')


@app.route("/test", methods=['GET', 'POST'])
@cross_origin()
def test():
    return "OK", 200


@app.route("/uploadImage", methods=['POST'])
@cross_origin()
def upload_image():
    if 'image-file' in request.files:
        image_data = request.files['image-file']
        pil_img = Image.open(image_data)
        pil_img.save("image.jpg", format="JPEG")
        cv2_img = cv2.imread("image.jpg")
        #
        response, status_code = run_for_my_life2(cv2_img)
        #
        os.remove("image.jpg")
        #
        return jsonify(response), status_code
    return jsonify({'message': 'failed'}), 200


if __name__ == '__main__':
    print("Model is loading")
    cropper, detector, reader = load_model()
    print("Model is ready!")
    app.run(debug=True, host='0.0.0.0', port=80)
