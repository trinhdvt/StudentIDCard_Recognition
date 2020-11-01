from detector.Detector import Detector
import cv2

# labels_path = "./obj.names"
label = ["id"]
config_path = "./config/detector_model.cfg"
# 1--xguD0tT37zG7P5mGoNaUBTp3RUgMqz # drive file id
weight_path = "./config/yolo-tinyv4-obj_best.weights"
test_img_path = "./test_img/thanh1.jpg"

detector = Detector(config_path, weight_path, label)
img = cv2.imread(test_img_path)
cropped_img, annotated_img = detector.predict(img)

assert cropped_img is not None

cv2.imwrite(f"./test_result/{test_img_path.split('/')[-1]}", annotated_img)
cv2.imshow("", annotated_img)
cv2.waitKey()
cv2.destroyAllWindows()
