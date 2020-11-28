from datetime import datetime
from firebase_admin import initialize_app, credentials, db
from utils import config

cred = credentials.Certificate(config.FIREBASE_KEY)
initialize_app(cred, {
    'databaseURL': config.FIREBASE_URL
})


def on_event(message):
    new_data = message.data
    if new_data is None:
        return
    new_mssv = new_data['mssv']
    snap = db.reference("/bai_giu_xe").order_by_child('mssv').equal_to(new_mssv).get()
    res = [(key, values) for key, values in snap.items()]
    bsx = None
    child_key = None
    for fb_key, value in res:
        if value['gio_ra'] == "":
            bsx = value['bsx']
            child_key = fb_key
    if bsx is None:
        print("Xe vao! Green LED is ON")
        db.reference("/bai_giu_xe").push({
            'bsx': new_data['bsx'],
            'bsx_img': new_data['bsx_img'],
            'gio_vao': new_data['time'],
            'gio_ra': "",
            'mssv': new_data['mssv'],
            'mssv_img': new_data['mssv_img']
        })
    elif bsx is not None:
        print("Xe ra! Checking!")
        if bsx == new_data['bsx']:
            print("Xe duoc phep ra! Green LED is ON")
            db.reference("/bai_giu_xe").child(child_key).update({
                'gio_ra': datetime.now().strftime("%d/%m/%Y %H:%M")
            })
        else:
            print("Warning warning! Yellow LED is ON! Check it out!")


if __name__ == '__main__':
    print("Server is listen for new data ...")
    db.reference("/newest_input").listen(on_event)
