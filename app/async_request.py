import json
import time
import grequests
from datetime import datetime
from utils import config, utils
from firebase_admin import initialize_app, credentials, db

# ---------------- INITIALIZE FIREBASE CONNECT --------------------
cred = credentials.Certificate(config.FIREBASE_KEY)
initialize_app(cred, {
    'databaseURL': config.FIREBASE_URL
})
newest_input = db.reference("/newest_input")
# -------------------- INITIALIZE REQUEST --------------------
request_data = [
    {
        'image': utils.cv2img_to_base64(img_path=None)
    },
    {
        'image': utils.cv2img_to_base64(img_path=None)
    }
]
request = (
    grequests.post(config.BSX_API_URL, data=request_data[0]),
    grequests.post(config.MSSV_API_URL, data=request_data[1])
)
t = time.time()
request = grequests.map(request)
t1 = time.time()
print(f"Took {t1 - t}")
# -------------------- PROCESS REQUEST RESPONSE --------------------
request_data = [json.loads(rq.text) for rq in request]
bsx_text = request_data[0]['bsx']
bsx_image = request_data[0]['image']
mssv_text = request_data[1]['mssv']
mssv_image = request_data[1]['image']
# -------------------- SEND TO NGHIAPHAM --------------------
bsx_path, mssv_path = utils.save_to_local((bsx_text, bsx_image), (mssv_text, mssv_image))
utils.to_web_storage(bsx_path, mssv_path)
# -------------------- SEND TO FIREBASE --------------------
new_data = {
    'mssv': mssv_text,
    'mssv_img': mssv_path,
    'bsx': bsx_text,
    'bsx_img': bsx_path,
    'time': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
}
newest_input.set(new_data)
