from datetime import datetime
from tools import config, utils
from firebase_admin import initialize_app, credentials, db
from threading import Thread
import json
import time
import grequests
import glob
import os

# ---------------- INITIALIZE FIREBASE CONNECT --------------------
cred = credentials.Certificate(config.FIREBASE_KEY2)
initialize_app(cred, {
    'databaseURL': config.FIREBASE_URL2
})


def insert_data(node_key: str, data: dict, push: bool):
    if push:
        db.reference(node_key).push(data)
    else:
        db.reference(node_key).set(data)


def handle_new_data(new_bsx, new_sv):
    send_start = time.time()
    # -------------------- PREPARE FOR REQUEST --------------------
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
    # -------------------- REQUEST RESPONSE --------------------
    process_start = time.time()
    request_data = [json.loads(rq.text) for rq in request]
    bsx_text = request_data[0]['bsx']
    bsx_image = request_data[0]['image']
    mssv_text = request_data[1]['mssv']
    mssv_image = request_data[1]['image']
    # -------------------- SEND TO LOCAL_WEB_SERVER --------------------
    bsx_path, mssv_path = utils.save_to_local((bsx_text, bsx_image), (mssv_text, mssv_image))
    utils.to_web_storage(bsx_path, mssv_path)
    process_end = time.time()
    print(f"Process time {process_end - process_start}")
    # -------------------- LOGIC ANALYST --------------------
    new_data = {
        'mssv': mssv_text,
        'imgIDCard': mssv_path.split("/")[-1],
        'bsx': bsx_text,
        'imgCar': bsx_path.split("/")[-1],
        'timeIn': datetime.now().strftime("%H:%M:%S %d-%m-%Y"),
        'timeOut': ""
    }
    #
    Thread(target=insert_data, args=("/input", new_data, False)).start()
    #
    snap = db.reference("/baixe").order_by_child("bsx").equal_to(new_data['bsx']).get()
    query_data = [(key, values) for key, values in snap.items()]
    #
    mssv, update_key = None, None
    for key, data in query_data:
        if data['timeOut'] == "":
            mssv = data['mssv']
            update_key = key
    #
    if mssv is not None:
        if mssv == new_data['mssv']:
            print("Xe ra hop le! Green LED is ON!")
            #
            Thread(target=utils.turn_led_on, args=('green',)).start()
            #
            db.reference("/baixe").child(update_key).update({
                'timeOut': new_data['timeOut']
            })
        else:
            print("Warning warning! Yellow LED is ON! Check it out!")
            #
            Thread(target=utils.turn_led_on, args=('yellow',)).start()
    else:
        # xe vao
        print("Xe vao! Green LED is ON!")
        Thread(target=utils.turn_led_on, args=('green',)).start()
        #
        Thread(target=insert_data, args=("/baixe", new_data, True)).start()
    #
    os.remove(new_bsx)
    os.remove(new_sv)


if __name__ == '__main__':
    while True:
        bsx_img = glob.glob(config.LISTEN_BSX_IMAGE + "*")
        mssv_img = glob.glob(config.LISTEN_MSSV_IMAGE + "*")
        if len(bsx_img) != 0 and len(mssv_img) != 0:
            bsx_path = bsx_img[-1]
            mssv_path = mssv_img[-1]
            if not utils.verify_img(bsx_path, mssv_path):
                continue
            print("Verify done!")
            start = time.time()
            handle_new_data(bsx_path, mssv_path)
            end = time.time()
            print(f"Total time {end - start}")
        time.sleep(1)
