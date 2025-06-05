import os
import requests
from dotenv import load_dotenv

load_dotenv()

CAT_API_URL=os.getenv('CAT_API_URL')

def get_cat_image() -> str:
    response = requests.get(CAT_API_URL)
    data = response.json()

    cat_image = data[0].get('url')

    return cat_image