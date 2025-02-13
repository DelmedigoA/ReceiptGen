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