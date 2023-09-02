import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import os
import random

imageRoot = "../corpus/final_fantasy_4"
outputRoot = "../tmp/"
imageFns = os.listdir(imageRoot)
random.shuffle(imageFns)
imageFn = imageFns[0]
imageFn = "2023072917271300-7E5C8E902A2AFEF28B1FE30BC0B2FB8A.jpg"

img = Image.open(os.path.join(imageRoot, imageFn))

# suggested by chatgpt for preprocessing the image
img = img.filter(ImageFilter.GaussianBlur(radius=1.0))
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(1.0)  # Adjust the enhancement factor as needed

img = img.convert("L")  # Convert to grayscale
threshold = 128  # Adjust the threshold as needed
img = img.point(lambda p: p > threshold and 255)


# Define the coordinates of the cropping region (left, upper, right, lower)
left = 255  # X-coordinate of the left edge of the cropping region
upper = 65  # Y-coordinate of the upper edge of the cropping region
right = 1000  # X-coordinate of the right edge of the cropping region
lower = 200  # Y-coordinate of the lower edge of the cropping region

# Crop the image
img = img.crop((left, upper, right, lower))

img.save(os.path.join(outputRoot, imageFn))

config = '--tessdata-dir "/Users/tmahrt/Downloads/tesseract_data"'
text = pytesseract.image_to_string(img, lang="jpn", config=config)
print(imageFn)
print(text.replace(" ", "").replace("\n", ""))
