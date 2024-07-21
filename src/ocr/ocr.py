import easyocr


def read_text_from_image(image_path):
    """
    使用EasyOCR库从图像中提取文本。
    image_path: 图像文件路径
    """
    reader = easyocr.Reader(['en', 'ch_sim'], gpu=True)  # 使用英语和简体中文模型
    return reader.readtext((image_path), detail=0)
