from utils.utils import base64_to_cv2img
from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
from cropper.Cropper import Cropper
from detector.Detector import Detector
from reader.Reader import Reader
from reader.Config import Cfg
from PIL import Image
import time

cropper = Cropper()
yolo_path = "../detector/config/detector_model.cfg"
yolo_weight = "../detector/config/detector_model.weights"
detector = Detector(yolo_path, yolo_weight)
reader_cfg = Cfg.load_config_from_file("../reader/tmp/cfg.yml")
reader_cfg['weights'] = '../reader/tmp/transformerocr2.pth'
reader_cfg['device'] = 'cpu'
reader = Reader(reader_cfg)

port = '8000'
app = Flask(__name__)
CORS(app)


@app.route("/")
@cross_origin()
def index():
    return "Welcome to Flask API"


@app.route("/id_recognize", methods=['POST'])
@cross_origin()
def run_for_your_life():
    start = time.time()
    img_b64 = request.form.get('image')
    img = base64_to_cv2img(img_b64)
    cropped = cropper.predict(img, resize=True)
    try:
        id_only_img, _ = detector.predict(cropped)
    except TypeError:
        return "Failed!"
    try:
        assert id_only_img is not None
        id_only_img = Image.fromarray(id_only_img)
        mssv = reader.predict(id_only_img)
        end = time.time()

        return_data = {
            'time': end - start,
            'result': mssv
        }
        return return_data
    except AssertionError:
        return "Failed!"


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=port)
