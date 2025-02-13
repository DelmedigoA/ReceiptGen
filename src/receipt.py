import random
from typing import List
import os
from PIL import Image, ImageDraw, ImageFont
import barcode
from barcode.writer import ImageWriter
from uuid import uuid4
from src.utils import *

class Receipt:
  def __init__(
      self,
      mode:str = "L",
      size: tuple = (300, 400),
      color: tuple = (255,),
      fonts_dir: str = "resources/hebrew/fonts",
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
      self.texts = [{"height": 0}]
      self.y = 0

  def reset(self):
      self.image = Image.new(mode=self.mode, size=self.size, color=self.color)
      self.draw = ImageDraw.Draw(self.image)
      self.w, self.h = self.image.size
      return None

  def add_text(self, text, x, font_size, fill=(0)):
      self.draw = ImageDraw.Draw(self.image)
      font = ImageFont.truetype(self.font_path, size=font_size)
      d = self.w - font.getlength(text)
      mult_fct = 1 / x
      x = int(d * mult_fct)
      self.draw.text(xy=(x, self.y), text=text, fill=fill, font=font, direction=self.direction)
      height = get_height(font, text)
      self.texts.append(dict(text=text,x=x,y=self.y,height=height))
      return None

  def bar_down(self, space=3):
      self.y += self.texts[-1]["height"] + space
      return None
  
  def add_barcode(self, space=3, width=150):
      number = str(uuid4())[:18] if random.random() >.5 else str(random.randint(1000000000000000,9999999999999999))
      barcode_obj = barcode.get_barcode_class("code39")
      my_ean = barcode_obj(number, writer=ImageWriter())
      my_ean.save("tmp",options={
          "background": (255,255,255),
          "foreground": (0,0,0),
          "text_distance": 8,
          "center_text": True,
          "font_path": "/content/ReceiptGen/resources/hebrew/fonts/cour.ttf",
          "quiet_zone": 1.0,
          "font_size": 16,
          "module_width": 0.25,
          "module_height": 20.0,
          })
      barcode_img = Image.open("tmp.png")
      os.remove("tmp.png")
      barcode_img = barcode_img.convert("L")
      new_width = width
      new_height = int(barcode_img.height * (new_width / barcode_img.width))
      barcode_img = barcode_img.resize((new_width, new_height)).rotate(0, fillcolor=(255,), expand=True)
      paste_y = self.y
      paste_x = (self.w - barcode_img.width) // 2
      self.image.paste(barcode_img, (paste_x, paste_y))
      return None
  
  def show(self):
      display(self.image)