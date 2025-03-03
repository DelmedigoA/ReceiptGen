import random
from typing import List
import os
from PIL import Image, ImageDraw, ImageFont
import barcode
from barcode.writer import ImageWriter
from uuid import uuid4
from .utils import get_height, get_random_date, get_random_telephone, get_product_id
from faker import Faker
import numpy as np

class BaseImage:
    """Base class for image creation and text rendering"""
    def __init__(
        self,
        mode: str = "L",
        size: tuple = (300, 400),
        color: tuple = (255, ),
        lang: str = "hebrew",
        direction: str = "rtl"
    ):
        self.lang = lang
        self.fonts_dir = f"resources/{self.lang}/fonts"
        self.mode = mode
        self.size = size
        self.color = color
        self.direction = direction
        self.image = Image.new(mode=self.mode, size=self.size, color=self.color)
        self.draw = ImageDraw.Draw(self.image)
        self.w, self.h = self.image.size
        self.font_path = random.choice(
            [os.path.join(self.fonts_dir, path) for path in os.listdir(self.fonts_dir) if path.endswith(".ttf")]
        )
        self.texts = [{"height": 0}]
        self.y = 0
        self.text_size = self.h // 60
    
    def reset(self):
        self.image = Image.new(mode=self.mode, size=self.size, color=self.color)
        self.draw = ImageDraw.Draw(self.image)
        self.w, self.h = self.image.size
        self.texts = [{"height": 0}]
        self.y = 0
    
    def add_text(self, text, x, font_size, fill=(0)):
        font = ImageFont.truetype(self.font_path, size=font_size)
        d = self.w - font.getlength(text)
        mult_fct = 1 / x
        x = int(d * mult_fct)
        self.draw.text(xy=(x, self.y), text=text, fill=fill, font=font, direction=self.direction)
        height = get_height(font, text)
        self.texts.append(dict(text=text, x=x, y=self.y, height=height))
    
    def bar_down(self, space=3):
        self.y += self.texts[-1]["height"] + space
    
    def crop_top_bottom_white_borders(self):
        arr = np.array(self.image)
        white_rows = np.all(arr == 255, axis=1)
        nonwhite = np.where(~white_rows)[0]
        if nonwhite.size == 0:
            return
        top = nonwhite[0]
        bottom = nonwhite[-1] + 1
        cropped = arr[top:bottom, :]
        self.image = Image.fromarray(cropped, 'L')
    
    def show(self):
        display(self.image)
