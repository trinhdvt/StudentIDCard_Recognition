import time
import numpy as np
import cv2
from flask import Flask, request
from flask_cors import CORS, cross_origin
from tools import config
from tools.loader import load_model
from tools.utils import base64_to_cv2img, cv2img_to_base64, cv2img_to_pil
from PIL import ImageDraw, ImageFont

global cropper
global detector
global reader

app = Flask(__name__)
CORS(app)


@app.route("/", methods=['GET', 'POST'])
@cross_origin()
def index():
    return "Hello World", 200


@app.route(config.MSSV_API_NAME, methods=['POST'])
@cross_origin()
def run_for_my_life():
    #
    start = time.time()
    # get data from request
    img_b64 = request.form.get('image')
    # convert base64 string to img
    origin_img = base64_to_cv2img(img_b64)
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
            #
            (x, y, w, h) = coordinate[key]
            draw_img = ImageDraw.Draw(cropped_img)
            draw_img.text((x, y - 5), text, fill=(255, 0, 0),
                          font=ImageFont.truetype(config.DISPLAY_FONT, 18))
    except Exception as e:
        print(e)
        return "", 406
    #
    end = time.time()
    # send back data
    cropped_img = cv2.cvtColor(np.array(cropped_img), cv2.COLOR_RGB2BGR)
    return_data = {
        'result': reader_rs,
        'time': end - start,
        'image': cv2img_to_base64(None, cropped_img, False).decode('utf-8')
        }
    return return_data, 200


if __name__ == '__main__':
    print("Model is loading")
    cropper, detector, reader = load_model()
    print("Model is ready!")
    app.run(debug=True, host=config.MSSV_API_ADDRESS, port=config.API_PORT)
