import random
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