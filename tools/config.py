# -------------------- SYSTEM CONFIG --------------------
import platform

ROOT_CONTENT = None
if ROOT_CONTENT is None:
    if platform.system() == 'Linux':
        ROOT_CONTENT = "/home/dvt/Desktop/StudentIDCard_Recognition"
    elif platform.system() == 'Windows':
        ROOT_CONTENT = "C:/Users/congp/Desktop/StudentIDCard_Recognition"
    else:
        raise Exception("OS not support!")
# -------------------- CROPPER CONFIG --------------------
IMG_WIDTH = 768
IMG_HEIGHT = 480
# -------------------- DETECTOR CONFIG --------------------
DETECTOR_CFG = f"{ROOT_CONTENT}/detector/config/detector_model.cfg"
DETECTOR_WEIGHT = f"{ROOT_CONTENT}/detector/config/detector_model.weights"
DETECTOR_WEIGHT_DRIVE_ID = "1KJ5gMSXaUPNoRKt9auEa2-EGC_zkA7XL"
DETECTOR_LABELS = f"{ROOT_CONTENT}/detector/config/labels"
# -------------------- READER CONFIG --------------------
READER_CFG = f"{ROOT_CONTENT}/reader/config/config.yml"
READER_WEIGHT = f"{ROOT_CONTENT}/reader/config/transformerocr3.pth"
READER_BACKUP_WEIGHT = f"{ROOT_CONTENT}/reader/config/transformerocr2.pth"
READER_WEIGHT_DRIVE_ID = "1_nhGbmnqxQMy0XYD2uVjWqKBQwNhAIZn"
READER_BACKUP_WEIGHT_DRIVE_ID = "1yTpMg07Xizg_rY9oHNyBmz7At-Uak2tS"
DEVICE = "cpu"
# -------------------- WEB_SERVER CONFIG --------------------
MSSV_API_NAME = "/id_recognize"
MSSV_API_ADDRESS = "0.0.0.0"
API_PORT = 8000
MSSV_API_URL = "http://0.0.0.0:8000/id_recognize"
BSX_API_URL = "http://192.168.43.98:8000/bsx"
# -------------------- WEB RESOURCE CONFIG --------------------
LOCAL_IMG_STORAGE = "/home/dvt/Desktop/pi_img/web_img/"
WEB_IMG_STORAGE = "/home/nghiapham/Desktop/Student-ID-Card-Identification-main2/src/img/"
# -------------------- SSH CONFIG --------------------
LISTEN_BSX_IMAGE = "/home/dvt/Desktop/pi_img/bsx/"
LISTEN_MSSV_IMAGE = "/home/dvt/Desktop/pi_img/sv/"
WEB_IP = "192.168.43.97"
# -------------------- FIREBASE CONFIG --------------------
FIREBASE_KEY = f"{ROOT_CONTENT}/app/config/db_key.json"
FIREBASE_URL = "https://student-id-card-identification.firebaseio.com/"
# -------------------- OTHER CONFIG --------------------
LED_API_URL = "http://192.168.43.213:8000/onLed"
