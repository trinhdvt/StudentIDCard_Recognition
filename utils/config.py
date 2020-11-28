ROOT_CONTENT = "/home/dvt/Desktop/StudentIDCard_Recognition"
# -------------------- CROPPER CONFIG --------------------
IMG_WIDTH = 768
IMG_HEIGHT = 480
# -------------------- DETECTOR CONFIG --------------------
DETECTOR_CFG = f"{ROOT_CONTENT}/detector/config/detector_model.cfg"
DETECTOR_WEIGHT = f"{ROOT_CONTENT}/detector/config/detector_model.weights"
# DETECTOR_WEIGHT_DRIVE_ID = "1--xguD0tT37zG7P5mGoNaUBTp3RUgMqz"
# -------------------- READER CONFIG --------------------
READER_CFG = f"{ROOT_CONTENT}/reader/config/cfg.yml"
READER_WEIGHT = f"{ROOT_CONTENT}/reader/config/transformerocr.pth"
BACKUP_READER_WEIGHT = f"{ROOT_CONTENT}/reader/config/transformerocr2.pth"
DEVICE = "cpu"
# -------------------- WEB_SERVER CONFIG --------------------
MSSV_API_NAME = "/id_recognize"
MSSV_API_ADDRESS = "0.0.0.0:8000"
MSSV_API_URL = f"http://{MSSV_API_ADDRESS}/{MSSV_API_NAME}"
BSX_API_NAME = "bsx"
BSX_API_IP = "192.168.137.254:8000"
BSX_API_URL = f"http://{BSX_API_IP}/{BSX_API_NAME}"
# -------------------- WEB RESOURCE CONFIG --------------------
LOCAL_IMG_STORAGE = "/home/dvt/Desktop/pi_img/web_img/"
WEB_IMG_STORAGE = "/home/nghiapham/Desktop/web-doan/src/img/"
# -------------------- SSH CONFIG --------------------
LISTEN_BSX_IMAGE = "/home/dvt/Desktop/pi_img/bsx/"
LISTEN_MSSV_IMAGE = "/home/dvt/Desktop/pi_img/sv/"
WEB_IP = "192.168.xxx.yyy"
# -------------------- FIREBASE CONFIG --------------------
FIREBASE_KEY = f"{ROOT_CONTENT}/app/key.json"
FIREBASE_URL = "https://test-fr-ee2c3.firebaseio.com/"
