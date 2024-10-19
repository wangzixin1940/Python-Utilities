import easyocr


def read_text_from_image(image_path):
    """
    Use the EasyOCR library to extract text from images.
    Args:
        image_path: Image file path
    Returns:
        Results
    """
    reader = easyocr.Reader(['en', 'ch_sim'], gpu=True)  # Use English and Chinese Simplified Chinese models
    return reader.readtext((image_path), detail=0)
