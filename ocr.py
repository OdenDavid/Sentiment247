import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

# Get the image given the path
def get_image(path):
    img = cv2.imread(path)
    return img

# Get the grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 225, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# Noise removal
def noise_removal(image):
    return cv2.medianBlur(image, 5)

# Get text
def ocr_core(img):
    text = pytesseract.image_to_string(img, lang='eng')
    return text

