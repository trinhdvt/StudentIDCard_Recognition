import glob
import cv2
from cropper.Cropper import Cropper

img_paths = glob.glob("../resized_img/*")
cropper = Cropper()
for fn in img_paths:
    cropped = cropper.predict(fn, True)
    cv2.imshow("", cropped)
    cv2.waitKey()
cv2.destroyAllWindows()
