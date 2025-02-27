import random
from PIL import Image
import numpy as np

def crop_white_borders(image):
    arr = np.array(image)
    white_rows = np.all(arr == 255, axis=1)
    nonwhite = np.where(~white_rows)[0]
    if nonwhite.size == 0:
        return image
    top = nonwhite[0]
    bottom = nonwhite[-1] + 1
    cropped = arr[top:bottom, :]
    return Image.fromarray(cropped, 'L')
    
def get_height(font, text):
      ascent, descent = font.getmetrics()
      (width, baseline), (offset_x, offset_y) = font.font.getsize(text)
      height = ascent - offset_y + descent
      return height

def get_max_height(font, text = "ן"):
      ascent, descent = font.getmetrics()
      (width, baseline), (offset_x, offset_y) = font.font.getsize(text)
      height = ascent - offset_y + descent
      return height

def get_random_telephone():
    kidomet = random.choice(["02", "03", "04", "05", "06", "07", "08", "09"])
    tel = random.randint(1000000,9999999)
    seperator = "" if random.random() > .5 else "-"
    return f"{kidomet}-{tel}"

def get_random_date():
    year = random.randint(2023, 2024)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    seperator = "/" if random.random() > .5 else "-"
    return f"{day}{seperator}{month}{seperator}{year}"

def get_product_id():
    first_digit = "7"
    number = str(random.randint(1e11,1e12))
    return first_digit + number