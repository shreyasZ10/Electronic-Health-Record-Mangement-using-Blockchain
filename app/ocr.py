import pytesseract as tess
tess.pytesseract.tesseract_cmd = r'C:\Users\SHREYAS\AppData\Local\Tesseract-OCR\tesseract.exe'
from PIL import Image
import cv2 
import numpy as np
# import matplotlib.pyplot as plt
from pytesseract import Output

# plt.switch_backend('Qt4Agg')

IMG_DIR = 'images/'

# scaling
def scaling(image):
    return cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image,5)
 
#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

#dilation
def dilate(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)
    
#erosion
def erode(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.erode(image, kernel, iterations = 1)

#opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

#canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)

#skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

#template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

 
# img = Image.open('report.jpg')
# text = tess.image_to_string(img)

# image = cv2.imread(IMG_DIR + 'report.jpg')
# b,g,r = cv2.split(image)
# rgb_img = cv2.merge([r,g,b])
# # plt.imshow(rgb_img)
# # plt.title('AUREBESH ORIGINAL IMAGE')
# # plt.show()

# # Preprocess image
    
# scaling_image = scaling(image)
# gray = get_grayscale(scaling_image)
# thresh = thresholding(gray)
# remove_noise_image = remove_noise(thresh)
# preprocessed_image = remove_noise_image

# print(tess.image_to_string(preprocessed_image))
# d = tess.pytesseract.image_to_data(preprocessed_image, output_type=Output.DICT)
# print(d['text'])
# print(tess.pytesseract.image_to_string(image))