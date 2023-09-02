''''
Image - from image format class, used to represent a PIL image. 
Image functions:
https://omz-software.com/pythonista/docs/ios/Image.html

'''

import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import os
import random

#Emeka's imageRoot
imageRoot = "/home/emeka/Documents/final_fantasy_4"
#Tim's imageRoot
# imageRoot = "../corpus/final_fantasy_4"
outputRoot = "/home/emeka/Documents/tmp/"

def grabRandomImage(rootPath):
    imageFns = os.listdir(rootPath)
    random.shuffle(imageFns)
    return imageFns[0]

# imageFn = grabRandomImage(imageRoot)
imageFn = "2023072917271300-7E5C8E902A2AFEF28B1FE30BC0B2FB8A.jpg"

#Image - 
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

#Emeka's dir
config = '--tessdata-dir "/home/emeka/Documents/tesseract_data"'

#Tim's dir
#config = '--tessdata-dir "/Users/tmahrt/Downloads/tesseract_data"'
text = pytesseract.image_to_string(img, lang="jpn", config=config)
print(imageFn)
print(text.replace(" ", "").replace("\n", ""))
