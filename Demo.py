from tools.loader import load_model
from tools.utils import cv2img_to_pil
from PIL import ImageDraw, ImageFont
from tools import config
import cv2

#
#
if __name__ == '__main__':
    cropper, detector, reader = load_model()
    #
    img = cv2.imread("./resized_img/tanh1.JPG")
    #
    cropped_img = cropper.predict(img, resize=True)
    detect_rs, annotated_img, coordinate = detector.predict(cropped_img, True)
    reader_rs = {}
    #
    cropped_img = cv2img_to_pil(cropped_img)
    for key, value in detect_rs.items():
        text = reader.predict(cv2img_to_pil(value))
        reader_rs[key] = text
        #
        (x, y, w, h) = coordinate[key]
        draw_img = ImageDraw.Draw(cropped_img)
        draw_img.text((x, y - 5), text,
                      font=ImageFont.truetype(config.DISPLAY_FONT, 18)
                      , fill=(255, 0, 0))

    #
    print(reader_rs)
    cropped_img.show()
