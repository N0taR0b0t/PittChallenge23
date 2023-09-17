import re
from enum import Enum
from google.cloud import vision


class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5


def extract_text_from_image(image_file):
    client = vision.ImageAnnotatorClient()

    with open(image_file, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)

    return response.full_text_annotation.text


def extract_ingredients_from_text(text):
    # Preprocessing: Remove content inside parentheses and any stray parentheses
    text_without_parentheses = re.sub(r'\([^)]*\)', '', text)

    # Further cleaning to remove unnecessary spaces and newlines
    clean_text = ' '.join(text_without_parentheses.split())

    # Use regex to find a comma-separated list of uppercase words/phrases
    matches = re.findall(r'\b([A-Z][A-Z\s\-]*(?:,\s*[A-Z][A-Z\s\-]*)+)\b', clean_text)

    return ', '.join([match for match in matches])


def get_image_ingredients(image_path):
    extracted_text = extract_text_from_image(image_path)
    ingredients = extract_ingredients_from_text(extracted_text)
    
    return ingredients


if __name__ == "__main__":
    input_image = "images/8.png"
    
    ingredients = get_image_ingredients(input_image)

    if ingredients:
        print(ingredients)
    else:
        print("No ingredients list found.")
