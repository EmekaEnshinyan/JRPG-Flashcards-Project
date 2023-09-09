''''
Image - from image format class, used to represent a PIL image. 
Image functions:
https://omz-software.com/pythonista/docs/ios/Image.html
'''

import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
#from google.cloud import translate
import os



def renameImage(rootPath):
    #return a list of elements where each el is the filename str
    # os.listdir('a') -> ['b.jpg', 'c.png', 'd.mp3']
    # os.path.join('a', 'b.jpg') -> 'a/b.jpg'
    imageFns = os.listdir(rootPath)
    
    #check if dir exists
    if not os.path.exists(rootPath):
        print(f"the directory '{rootPath}' does not exist.")
        return
    for i in imageFns:
        pass


def extractTextFromImages(path):
    #open an image 
    # os.path.join('a', 'b', 'c.png') -> '/a/b/c.png'
    for imageName in os.listdir(path):
        fullPath = os.path.join(path, imageName)
        #a lazy operation: "bookmarks" images and does not actually open them
        img = Image.open(fullPath)
    
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
        img.save(os.path.join(outputRoot, imageName)) # TODO: Watch out this is a global variable

        #Emeka's dir
        config = '--tessdata-dir "/home/emeka/Documents/tesseract_data"'

        #Tim's dir
        #config = '--tessdata-dir "/Users/tmahrt/Downloads/tesseract_data"'
        text = pytesseract.image_to_string(img, lang="jpn", config=config)
        print()
        print(text.replace(" ", "").replace("\n", ""))
        print("\n\n")


    

'''
def translate_text(target
Image - from image format class, used to represent a PIL image. 
Image functions:
https://omz-software.com/pythonista/docs/ios/Image.html
'''

def translate_text(target: str, text: str) -> dict:
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)

    print("Text: {}".format(result["input"]))
    print("Translation: {}".format(result["translatedText"]))
    print("Detected source language: {}".format(result["detectedSourceLanguage"]))

    return result


if __name__ == "__main__":
    
    #Emeka's imageRoot
    imageRoot = "/home/emeka/Documents/final_fantasy_4"
    outputRoot = "/home/emeka/Documents/tmp/"
    renameImage(imageRoot)
    for filename in os.listdir(imageRoot):
        extractTextFromImage(os.path.join(imageRoot, filename))
