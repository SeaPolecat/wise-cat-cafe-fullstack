import os
import requests
from dotenv import load_dotenv
import easyocr

load_dotenv()

CAT_API_URL = os.getenv('CAT_API_URL')
INSPIROBOT_API_URL = os.getenv('INSPIROBOT_API_URL')


def get_cat_image() -> str:
    response = requests.get(CAT_API_URL)
    data = response.json() # response is given in json format

    # extract image url from the json
    cat_image = data[0].get('url')

    return cat_image


def get_wisdom() -> str:
    response = requests.get(INSPIROBOT_API_URL)
    wisdom_image = response.text # api only gives an image
    wisdom_text = '' # the actual text

    # setup ocr reader (configure language to be english)
    reader = easyocr.Reader(['en'])

    # use reader to extract text from the image
    ocr_result = reader.readtext(wisdom_image)

    # result is a list, so process it to get the full text
    for word in ocr_result:
        wisdom_text += word[1] + ' '

    return wisdom_text.strip()