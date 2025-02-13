import random
from typing import List
import os
from PIL import Image, ImageDraw, ImageFont
import barcode
from barcode.writer import ImageWriter
from uuid import uuid4
from src.utils import get_height, get_random_date, get_random_telephone
from faker import Faker

class Receipt:
    def __init__(
        self,
        mode: str = "L",
        size: tuple = (300, 400),
        color: tuple = (255, ),
        lang: str = "hebrew"
    ):
        self.lang = lang
        self.fonts_dir = f"resources/{self.lang}/fonts"
        self.mode = mode
        self.size = size
        self.color = color
        self.direction = "rtl" if self.lang == "he" else "ltr"
        self.image = Image.new(mode=self.mode, size=self.size, color=self.color)
        self.draw = ImageDraw.Draw(self.image)
        self.w, self.h = self.image.size
        self.font_path = random.choice(
            [os.path.join(self.fonts_dir, path) for path in os.listdir(self.fonts_dir) if path.endswith(".ttf")]
        )
        self.texts = [{"height": 0}]
        self.y = 0
        self.fake = Faker("he_IL")
        self.set_products()
        self.set_stores()

    def set_products(self):
        with open(f"/content/ReceiptGen/resources/{self.lang}/products/names.txt", "r") as file:
            text = file.read()
            products = text.split("\n")
            random.shuffle(products)
            self.products = list(set([p.strip().replace("  ", " ") for p in products if len(p) < 20]))
    
    def set_stores(self):
        with open(f"/content/ReceiptGen/resources/{self.lang}/stores/names.txt", "r") as file:
            text = file.read()
            stores = text.split("\n")
            random.shuffle(stores)
            stores = list(set([s.strip().replace("  ", " ") for s in stores]))
        self.israel_supermarkets = stores

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
        self.texts.append(dict(text="BARCOD", x=paste_x, y=self.y, height=new_height))

    def show(self):
        display(self.image)

    def add_date(self):
        self.bar_down(random.randint(0, self.h // 100))
        self.add_text(text=get_random_date(), x=random.choice([100, 2, 1]), font_size=self.h // 43)
    
    def add_entity(self):
        self.bar_down(10)
        self.add_text(text=random.choice(self.israel_supermarkets), x=random.choice([2]), font_size=self.h // 23)
    
    def add_summary(self):
        self.bar_down(random.randint(0, self.h // 40))
        base_total_str = "{:.2f}".format(self.total_without_maam)
        self.add_text(text="תשלום ללא מעמ                         " + base_total_str, x=random.choice([2]), font_size=self.h // 43)
        self.bar_down(random.randint(0, self.h // 40))
        final_total = self.total_without_maam * 1.18  # adding 18.0% VAT
        final_total_str = "{:.2f}".format(final_total)
        self.add_text(text="סהכ לתשלום                        " + final_total_str, x=random.choice([2]), font_size=self.h // 43)
    
    def add_dotted_lines_before_table(self):
        self.bar_down(random.randint(0, self.h // 20))
        self.add_text(text=" ".join(["-"] * (self.h // 3)), x=random.choice([2]), font_size=self.h // 43)
    
    def add_table(self):
        prod_list = self.products
        self.bar_down(random.randint(0, self.h // 10))
        columns = ["תיאור", "מחיר", "כמות", "לתשלום"]
        xs = [1.15, 2, 3, 10]
        for x, col in zip(xs, columns):
            self.add_text(text=col, x=x, font_size=14)
        self.bar_down()
        for x, col in zip(xs, columns):
            self.add_text(text=(len(col) + 2) * "-", x=x, font_size=14)
        product_names = random.choices(prod_list, k=8)
        random.shuffle(product_names)
        product_prices = ["{:.2f}".format(random.uniform(1, 10)) for _ in range(len(product_names))]
        quantities = [random.randint(1, 5) for _ in range(len(product_names))]
        prod_items = []
        for name, price, quantity in zip(product_names, product_prices, quantities):
            prod_items.append({"name": name, "price": price, "quantity": quantity})
        self.total_without_maam = 0.0  # initialize the sum before VAT
        self.bar_down(random.randint(0, self.h // 20))
        b_down = random.randint(0, self.h // 30)
        for product in prod_items:
            self.add_text(text=product["price"], x=2, font_size=14)
            self.add_text(text=str(product["quantity"]), x=3, font_size=14)
            row_total = float(product["price"]) * product["quantity"]
            self.total_without_maam += row_total
            row_total_str = "{:.2f}".format(row_total)
            self.add_text(text=" ₪" + row_total_str, x=10, font_size=12)
            self.add_text(text=product["name"], x=1.15, font_size=14)
            self.bar_down(b_down)
    
    def add_domain(self):
        self.bar_down(5)
        self.add_text(text=self.fake.domain_name(), x=random.choice([2]), font_size=self.h // 43)
    
    def add_detailes(self):
        self.bar_down(5)
        self.bar_down(5)
        self.add_text(text=f"טל׳ {get_random_telephone()}", x=random.choice([2]), font_size=self.h // 43)
        self.bar_down(5)
        self.add_text(text=f"פקס: {get_random_telephone()}", x=random.choice([2]), font_size=self.h // 43)
        self.bar_down(5)
        self.add_text(text=self.fake.address().replace("(", "").replace(")", ""), x=random.choice([2]), font_size=self.h // 43)
        self.bar_down(5)
        self.add_text(text=self.fake.ascii_company_email(), x=random.choice([2]), font_size=self.h // 43)
    
    def add_receipt_id(self):
        self.bar_down(5)
        self.add_text(text=random.choice(["קבלה:", "-קב'", "מס' חשבון קבלה", "מספר חשבון", "מס' חשבונית"]), x=random.choice([1.28]), font_size=self.h // 43)
        self.add_text(text=str(random.randint(10000,99999)), x=random.choice([2]), font_size=self.h // 43)
    
    def add_branch(self):
        self.bar_down(7)
        self.add_text(text=random.choice(["סניף:", "-סנ'", ":מס סניף", ":מס' הסניף", "מספר סניף"]), x=random.choice([1.28]), font_size=self.h // 43)
        self.add_text(text=str(random.randint(0,1000)), x=random.choice([2.5]), font_size=self.h // 50)

    def add_checkout(self, bar_down=False):
        self.bar_down(7) if not bar_down else None
        self.add_text(text=random.choice(["קופה:", "-קו'", ":מס קופה", ":מס' הקופה", "מספר קופה"]), x=random.choice([4]), font_size=self.h // 43)
        self.add_text(text=str(random.randint(0,30)), x=random.choice([7]), font_size=self.h // 50)

    def do_nothing(self):
        pass
