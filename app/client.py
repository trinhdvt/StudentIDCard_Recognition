import grequests
import json
import cv2
from tools import utils, config

img_path = "/test_img/101180012.jpeg"
data = {
    'image': utils.cv2img_to_base64(img_path)
    }
rs = [grequests.post(config.MSSV_API_URL, data=data)]

rs = grequests.map(rs)
assert rs[0].status_code == 200, "Failed"
data = json.loads(rs[0].text)
print(data['result'])
print(data['time'])
cv2.imshow("", utils.base64_to_cv2img(data['image']))
cv2.waitKey()
cv2.destroyAllWindows()
