import grequests
import json
import base64
from PIL import Image
from io import BytesIO


def img_to_b64(file_path):
    img = Image.open(file_path)
    im_file = BytesIO()
    img.save(im_file, format='JPEG')
    im_bytes = im_file.getvalue()
    b64 = base64.b64encode(im_bytes)
    return b64


def b64_to_pil(b64_encoded):
    b64_decoded = base64.b64decode(b64_encoded)
    im_file = BytesIO(b64_decoded)
    img = Image.open(im_file)
    return img


if __name__ == '__main__':
    img_path = "../test_img/9mp.jpg"
    data = {
        'image': img_to_b64(img_path)
    }
    rs = [grequests.post("http://127.0.0.1:8000/id_recognize", data=data)]
    #
    rs = grequests.map(rs)
    assert rs[0].status_code == 200, "Failed"
    #
    data = json.loads(rs[0].text)
    #
    print(data['result'])
    print(data['time'])
    img_rs = b64_to_pil(data['image'])
    img_rs.show()
