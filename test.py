import cv2
import pytesseract


tessdata_config = r'--oem 1 --psm 7 tessdata_best'

# Load the image
image_path = 'Sample_Image/h2.jpg'
image = cv2.imread(image_path)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply adaptive thresholding to preprocess the image
# gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 7)

# Perform OCR to detect text
# text = pytesseract.image_to_string(gray)
text = pytesseract.image_to_string(gray)

# Print the detected text
print(text)
