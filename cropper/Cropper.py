import cv2
import imutils
import numpy as np


class Cropper:
    """
    Cắt vùng thẻ sinh viên ra khỏi background ảnh đầu vào
    """

    def __init__(self):
        pass

    def sort_by_area(self, contour):
        (_, _, w, h) = cv2.boundingRect(contour)
        return w * h

    def find_four_corner(self, img):
        """

        :param img: Ảnh chứa thẻ sinh viên
        :return: Toạ độ 4 góc thẻ (top_left -> top_right -> bottom_right -> bottom_left)
        """
        # remove noise with Gaussian Filter kernel size = (5,5)
        img = cv2.GaussianBlur(img, (5, 5), 0)
        # cvt img to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # apply threshold for detect ROI (Regions of Interest)
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 3)
        # find all contours
        contours = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        # grab contours
        contours = imutils.grab_contours(contours)
        # sort all contours follow by area increasing
        contours = sorted(contours, key=self.sort_by_area, reverse=True)
        # the biggest one is the whole img, the second one is our ROI
        c = contours[1]
        # calculate arc length of selected contour
        peri = cv2.arcLength(c, True)
        # approximate the shape of contour with variety of points
        approx = cv2.approxPolyDP(c, 0.01 * peri, True)
        approx = np.asarray([p[0] for p in approx])
        # sum x + y
        sum_approx = np.sum(approx, axis=1)
        # diff y - x
        diff_approx = np.diff(approx, axis=1)
        corner_point = np.array([
            # [-20, -20]: padding
            # top_left point has smallest sum
            approx[np.argmin(sum_approx)] + [-20, -20],
            # top_right point has smallest diff
            approx[np.argmin(diff_approx)] + [20, -20],
            # bottom_right
            approx[np.argmax(sum_approx)] + [20, 20],
            # bottom_left
            approx[np.argmax(diff_approx)] + [-20, 20],
        ], dtype="float32")
        return corner_point

    def calculate_fit_size(self, corner_pts):
        """

        :param corner_pts: Toạ độ 4 góc
        :return: Size tương ứng
        """
        (tl, tr, br, bl) = corner_pts
        # width = distance between top_left and top_right
        # or bottom_right and bottom_left
        width1 = np.sqrt((tl[0] - tr[0]) ** 2 + (tl[1] - tr[1]) ** 2)
        width2 = np.sqrt((bl[0] - br[0]) ** 2 + (bl[1] - br[1]) ** 2)
        new_width = max(int(width1), int(width2))
        #
        height1 = np.sqrt((tl[0] - bl[0]) ** 2 + (tl[1] - bl[1]) ** 2)
        height2 = np.sqrt((tr[0] - br[0]) ** 2 + (tr[1] - br[1]) ** 2)
        new_height = max(int(height1), int(height2))
        #
        return new_width, new_height

    def transform_img(self, img_path, resize=False):
        """

        :param img_path: Đường dẫn tới file ảnh đầu vào
        :param resize: True if size of img > (1280, 720)
        :return: ảnh chỉ chứa thẻ sinh viên
        """
        img = cv2.imread(img_path)
        (h, w, c) = img.shape
        if resize and (w, h) > (1280, 720):
            if w > h:
                img = cv2.resize(img, (1280, 720))
            else:
                img = cv2.resize(img, (720, 1280))
        # get four corner coordinates
        four_corner = self.find_four_corner(img)
        # calculate size for output img
        width, height = self.calculate_fit_size(four_corner)
        # rotate img
        dst_point = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype="float32")
        M = cv2.getPerspectiveTransform(four_corner, dst_point)
        warped = cv2.warpPerspective(img, M, (width, height))
        return warped

    def predict(self, img_path: str, resize=False):
        return self.transform_img(img_path, resize)