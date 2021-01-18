# -------------------- SYSTEM CONFIG --------------------
ROOT_CONTENT = "/Users/trinhdvt/Desktop/StudentIDCard_Recognition"
# -------------------- CROPPER CONFIG --------------------
IMG_WIDTH = 768
# -------------------- DETECTOR CONFIG --------------------
DETECTOR_CFG = f"{ROOT_CONTENT}/detector/config/detector_model.cfg"
DETECTOR_WEIGHT = f"{ROOT_CONTENT}/detector/config/detector_model.weights"
DETECTOR_WEIGHT_DRIVE_ID = "1xoO3xFSZ4KnCs4IRX3l4MyBGPVd4pmWb"
DETECTOR_LABELS = f"{ROOT_CONTENT}/detector/config/labels"
DISPLAY_FONT = f"{ROOT_CONTENT}/detector/config/Montserrat-SemiBold.ttf"
# -------------------- READER CONFIG --------------------
READER_CFG = f"{ROOT_CONTENT}/reader/config/config.yml"
READER_WEIGHT = f"{ROOT_CONTENT}/reader/config/transformerocr.pth"
READER_WEIGHT_DRIVE_ID = "1k08K0f-r6VOGvlZ1EyF4DL6MdnOJX_PK"
DEVICE = "cpu"
# -------------------- WEB_SERVER CONFIG --------------------
MSSV_API_NAME = "/id_recognize"
MSSV_API_ADDRESS = "127.0.0.1"
API_PORT = 8000
MSSV_API_URL = "http://127.0.0.1:8000/id_recognize"
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
