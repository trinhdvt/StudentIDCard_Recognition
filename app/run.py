import json
import time
import grequests
from datetime import datetime
from utils import config, utils
from firebase_admin import initialize_app, credentials, db
import glob

# ---------------- INITIALIZE FIREBASE CONNECT --------------------
cred = credentials.Certificate(config.FIREBASE_KEY)
initialize_app(cred, {
    'databaseURL': config.FIREBASE_URL
})
newest_input = db.reference("/newest_input")


def handle_new_data(new_bsx, new_sv):
    send_start = time.time()
    # -------------------- INITIALIZE REQUEST --------------------
    request_data = [
        {
            'image': utils.cv2img_to_base64(img_path=new_bsx)
        },
        {
            'image': utils.cv2img_to_base64(img_path=new_sv)
        }
    ]
    request = (
        grequests.post(config.BSX_API_URL, data=request_data[0]),
        grequests.post(config.MSSV_API_URL, data=request_data[1])
    )
    request = grequests.map(request)
    send_done = time.time()
    print(f"Time for send request {send_done - send_start}")
    # -------------------- PROCESS REQUEST RESPONSE --------------------
    process_start = time.time()
    request_data = [json.loads(rq.text) for rq in request]
    bsx_text = request_data[0]['bsx']
    bsx_image = request_data[0]['image']
    mssv_text = request_data[1]['mssv']
    mssv_image = request_data[1]['image']
    # -------------------- SEND TO NGHIAPHAM --------------------
    bsx_path, mssv_path = utils.save_to_local((bsx_text, bsx_image), (mssv_text, mssv_image))
    utils.to_web_storage(bsx_path, mssv_path)
    process_end = time.time()
    print(f"Process time {process_end - process_start}")
    # -------------------- SEND TO FIREBASE --------------------
    upload_start = time.time()
    new_data = {
        'mssv': mssv_text,
        'mssv_img': mssv_path.split("/")[-1],
        'bsx': bsx_text,
        'bsx_img': bsx_path.split("/")[-1],
        'time': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    newest_input.set(new_data)
    upload_done = time.time()
    print(f"Upload time {upload_start - upload_start}")


if __name__ == '__main__':
    bsx_img = glob.glob(config.LISTEN_BSX_IMAGE + "*")
    mssv_img = glob.glob(config.LISTEN_MSSV_IMAGE + "*")
    if len(bsx_img) != 0 and len(mssv_img) != 0:
        start = time.time()
        bsx_path = bsx_img[-1]
        mssv_path = mssv_img[-1]
        handle_new_data(bsx_path, mssv_path)
        end = time.time()
        print(f"Total time {end - start}")
