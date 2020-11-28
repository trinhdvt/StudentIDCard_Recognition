import numpy as np
import cv2
import time
import os
from utils.utils import download_model


class Detector:
    def __init__(self, cfg_path, weight_path, labels=None):
        if labels is None:
            labels = ['id']
        self.cfg_path = cfg_path
        self.weight_path = weight_path
        if not os.path.exists(weight_path):
            download_model("detector")
        self.IMG_WIDTH = 608
        self.IMG_HEIGHT = 608
        self.labels = labels
        self.net = cv2.dnn.readNetFromDarknet(self.cfg_path, self.weight_path)
        self.ln = self.net.getLayerNames()
        self.ln = [self.ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

    def preprocess_image(self, img):
        # img = cv2.resize(img, (self.IMG_WIDTH, self.IMG_HEIGHT))
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

        if show_time:
            start = time.time()
        output = self.net.forward(self.ln)
        if show_time:
            end = time.time()
            print(f"Time = {end - start}")
        boxes = []
        confidences = []
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

        boxes_idx = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)
        if len(boxes_idx) > 0:
            cropped_img = None
            for i in boxes_idx.flatten():
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                cropped_img = clone_img[y:y + h, x:x + w]
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(img, "id", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            return cropped_img, img
