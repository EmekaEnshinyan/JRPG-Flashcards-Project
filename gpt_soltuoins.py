import os
import shutil

def rename_jpg_files(directory):
    # Check if the provided directory exists
    if not os.path.exists(directory):
        print(f"The directory '{directory}' does not exist.")
        return

    # List all files in the directory
    files = os.listdir(directory)

    # Iterate through the files
    for filename in files:

        if filename.endswith(".jpg"):
            filenumerator = "0"
            # Construct the new filename as you desire
            new_filename = filenumerator + filename  # You can customize the new name here

            # Build the full paths for the old and new filenames
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_filename)

            # Rename the file
            try:
                shutil.move(old_path, new_path)
                print(f"Renamed '{filename}' to '{new_filename}'")
            except Exception as e:
                print(f"Error renaming '{filename}': {e}")
            filenumerator += filenumerator

if __name__ == "__main__":
    directory = "/path/to/your/directory"  # Replace with the directory path containing your .jpg files
    rename_jpg_files(directory)


'''
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

'''
