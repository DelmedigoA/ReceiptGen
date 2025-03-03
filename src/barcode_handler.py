from uuid import uuid4
import random
import barcode
from barcode.writer import ImageWriter
from PIL import Image
import os


class BarcodeHandler:
    """Class for barcode-specific functionality"""
    def add_barcode(self, space=3, width=300):
        self.bar_down(5)
        number = str(uuid4())[:18] if random.random() > .5 else str(random.randint(1000000000000000, 9999999999999999))
        barcode_obj = barcode.get_barcode_class("code39")
        my_ean = barcode_obj(number, writer=ImageWriter())
        my_ean.save("tmp", options={
            "background": (255, 255, 255),
            "foreground": (0, 0, 0),
            "text_distance": 8,
            "center_text": True,
            "font_path": self.font_path,
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
        barcode_img = barcode_img.resize((new_width, new_height))
        paste_y = self.y
        paste_x = (self.w - barcode_img.width) // 2
        self.image.paste(barcode_img, (paste_x, paste_y))
        self.texts.append(dict(text="BARCOD", x=paste_x, y=self.y, height=new_height))
        self.data.append({"barcode_number": number})