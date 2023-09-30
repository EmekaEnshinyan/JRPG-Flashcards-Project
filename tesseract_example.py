''''
Image - from image format class, used to represent a PIL image. 
Image functions:
https://omz-software.com/pythonista/docs/ios/Image.html
'''

import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
#from google.cloud import translate
import os
import openpyxl as opx
import shutil
import pandas as pd


#when need to read the csv file
def readCVS(csvPath):
    pd.read_csv(csvPath)

def rename_jpg_files(directory):
    # Check if the provided directory exists
    numerator = "1"
    if not os.path.exists(directory):
        print(f"The directory '{directory}' does not exist.")
        return
    # List all files in the directory
    files = os.listdir(directory)
    for filename in files:
        if filename.endswith(".jpg"):
            # Construct the new filename as you desire
            new_filename = numerator + ".jpg" # You can customize the new name here 00, 01
            # Build the full paths for the old and new filenames
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_filename) #->0.jpg
            # Rename the file
            try:
                shutil.move(old_path, new_path)
                print(f"Renamed '{filename}' to '{new_filename}'")
            except Exception as e:
                print(f"Error renaming '{filename}': {e}")
            #convert filename to int
            #increment by 1
            #convert back to string
            numerator = int(numerator) # '1'
            numerator += 1 # 2
            numerator = str(numerator) # '2'

def extractTextFromImages(path, preprocessedImagePath, outputFilename):
    #open an image 
    # os.path.join('a', 'b', 'c.png') -> '/a/b/c.png'
    ocredTexts = []
    for imageName in os.listdir(path):
        fullPath = os.path.join(path, imageName)
        if imageName[-1] != 'g':
            continue
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
        img.save(os.path.join(preprocessedImagePath, imageName))

        #Emeka's dir
        config = '--tessdata-dir "/home/emeka/Documents/tesseract_data"'

        #Tim's dir
        #config = '--tessdata-dir "/Users/tmahrt/Downloads/tesseract_data"'
        text = pytesseract.image_to_string(img, lang="jpn", config=config)
        print()
        print(text.replace(" ", "").replace("\n", ""))
        print("\n\n")
        ocredTexts.append(text)

    with open(outputFilename, "w") as fd: # when with block exits, will invoke a cleanup method file descriptor (address in memory of file)
        for textInfo in ocredTexts:
            number = str(textInfo[0])
            #name = textInfo[1]
            text = textInfo[1]
            cleanedText = text.replace(" ", "").replace("\n", "")
            
            #examples of how to join the strings
            # 1. (name) text
            # number + " " + name + " " + text
            # " ".join([number, name, text])
            # f"{number} {name} {text}"

            fd.write(f"{number}. {cleanedText}")
            fd.write("\n")

    # with open(outputFilename, "r") as fd:
    #     fileText = fd.read()
    #     for line in fd.readlines():
    #         print(line)
    

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
    outputRoot = "/home/emeka/Documents/JRPG-Flashcards-Project/output" # ouput <=> output
    preprocessedImagePath = "/home/emeka/Documents/JRPG-Flashcards-Project/tmp"

    extractOcrText = os.path.join(outputRoot, "ocred_text.txt")
    
    #loop over the files in imageRoot
    #check if each name is what is expected
    #yes -> leave it alone
        #reame to what we want
    
    #rename_jpg_files(imageRoot)
    extractTextFromImages(imageRoot, preprocessedImagePath, extractOcrText)

    
    
    
    
    
    
    
    
    '''
    for filename in os.listdir(imageRoot):
        texttoexcel = extractTextFromImages(os.path.join(imageRoot, filename))
    #send text to excel sheet
    workbook = opx.Workbook()
    sheet = workbook.active
    for column in workbook:
        #converts str to int, increment by 1, convert back to str
        col = '1'    
        #a(num)
        #increment by 1
        cellvalue = 'a{}'.format(col)
        sheet[cellvalue] = texttoexcel
        reg = re.search(r"\d+", col)
        str(int(reg) + 1)
    '''
    
    #provide dir for excel file below