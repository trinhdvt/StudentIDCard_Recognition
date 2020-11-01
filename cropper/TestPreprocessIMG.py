import cv2
import imutils

img = cv2.imread("../detector/test_img/huy2_0_143.JPG")
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
cv2.drawContours(img, contours, -1, (0, 255, 0), 1)
cv2.imshow("", img)
cv2.waitKey()
cv2.destroyAllWindows()
