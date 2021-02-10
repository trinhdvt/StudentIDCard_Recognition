import os

# -------------------- SYSTEM CONFIG --------------------
ROOT_CONTENT = os.getcwd()
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
