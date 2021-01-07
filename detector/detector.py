import numpy as np
import cv2
import time
import os
from tools.utils import download_model, parse_img_size


class Detector:
    def __init__(self, cfg_path, weight_path, labels_path=None):
        assert os.path.exists(cfg_path), "Config file not found"
        assert os.path.exists(labels_path), "Labels file not found"
        #
        self.cfg_path = cfg_path
        self.weight_path = weight_path
        self.classes = open(labels_path).read().strip().split("\n")
        #
        if not os.path.exists(weight_path):
            download_model("detector")
        #
        self.IMG_WIDTH, self.IMG_HEIGHT = parse_img_size(self.cfg_path)
        self.net = cv2.dnn.readNetFromDarknet(self.cfg_path, self.weight_path)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.ln = self.net.getLayerNames()
        self.ln = [self.ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

    def preprocess_image(self, img):
        blob_img = cv2.dnn.blobFromImage(img, 1 / 255.0,
                                         (self.IMG_WIDTH, self.IMG_HEIGHT),
                                         swapRB=True, crop=False)
        return blob_img

    def predict(self, origin_img, show_time=False):
        img = origin_img.copy()
        blob_img = self.preprocess_image(img)
        clone_img = img.copy()
        (origin_h, origin_w) = img.shape[:2]
        self.net.setInput(blob_img)

        start = time.time()
        output = self.net.forward(self.ln)
        end = time.time()
        if show_time:
            print(f"Time = {end - start}")
        # ------------------------ OUTPUT FROM YOLO ------------------------
        boxes = []
        confidences = []
        classIDs = []
        for out in output:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    box = detection[0:4] * np.array([origin_w, origin_h, origin_w, origin_h])
                    (centerX, centerY, width, height) = box.astype("int")

                    x = int(centerX - width / 2)
                    y = int(centerY - height / 2)
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(class_id)
        # ------------------------ NON-MAX SUPPRESSION ------------------------
        boxes_idx = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        #
        np.random.seed(42)
        colors = np.random.randint(0, 255, size=(len(self.classes), 3), dtype='uint8')
        #
        if len(boxes_idx) > 0:
            result = {}
            coordinate = {}
            for i in boxes_idx.flatten():
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                #
                color = [int(c) for c in colors[classIDs[i]]]
                class_name = self.classes[classIDs[i]]
                if class_name == 'name':
                    h -= 5
                    y += 5
                cropped_img = clone_img[y:y + h, x:x + w]
                result[class_name] = cropped_img

                coordinate[class_name] = (x, y, w, h)
                #
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                text = "{}: {:.4f}".format(class_name, confidences[i])
                cv2.putText(img, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
            #
            # return cropped_img, img
            return result, img, coordinate
