import random
from typing import List
import os
from PIL import Image, ImageDraw, ImageFont

class Receipt:
  def __init__(
      self,
      mode:str = "L",
      size: tuple = (300, 400),
      color: tuple = (255,),
      fonts_dir: str = "resources/fonts",
      lang: str = "he"
      ):
    self.mode = mode
    self.size = size
    self.color = color
    self.direction = "rtl" if lang == "he" else "ltr"
    self.image = Image.new(mode=self.mode, size=self.size, color=self.color)
    self.draw = ImageDraw.Draw(self.image)
    self.w, self.h = self.image.size
    self.font_path = random.choice([os.path.join(fonts_dir, path) for path in os.listdir(fonts_dir) if path.endswith(".ttf")])
  
  def reset(self):
    self.image = Image.new(mode=self.mode, size=self.size, color=self.color)
    self.draw = ImageDraw.Draw(self.image)
    self.w, self.h = self.image.size
  
  def add_text(self, text, x, y, is_bold, font_size, fill=(0)):
      self.draw = ImageDraw.Draw(self.image)
      font = ImageFont.truetype(self.font_path, size=font_size)
      d = self.w - font.getlength(text)
      mult_fct = 1 / x
      x = int(d * mult_fct)
      self.draw.text(xy=(x, y), text=text, fill=fill, font=font, direction=self.direction)
      return None