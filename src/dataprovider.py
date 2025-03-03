from faker import Faker
import random

class DataProvider:
    """Class for managing data sources like products and stores"""
    def __init__(self, lang="hebrew"):
        self.lang = lang
        self.fake = Faker("he_IL")
        self.products = []
        self.israel_supermarkets = []
        self.set_products()
        self.set_stores()
    
    def set_products(self):
        with open(f"resources/{self.lang}/products/names.txt", "r") as file:
            text = file.read()
            products = text.split("\n")
            random.shuffle(products)
            self.products = list(set([p.strip().replace("  ", " ") for p in products if len(p) < 20]))
    
    def set_stores(self):
        with open(f"resources/{self.lang}/stores/names.txt", "r") as file:
            text = file.read()
            stores = text.split("\n")
            random.shuffle(stores)
            self.israel_supermarkets = list(set([s.strip().replace("  ", " ") for s in stores]))