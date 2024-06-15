import easyocr

def read_text_from_image(image_path):
    """
    Use the easy ocr library to extract text from images.
    image_path: image file path
    """
    reader = easyocr.Reader(['en', 'ch_sim'], gpu=True) # Use English and Simplified Chinese models
    return reader.readtext((image_path), detail=0)

