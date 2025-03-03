import random
from .utils import *

class ReceiptElements:
    """Class for receipt-specific elements"""
    def add_date(self):
        self.bar_down(random.randint(0, self.h // 100))
        self.add_text(text=get_random_date(), x=random.choice([100, 2, 1]), font_size=self.text_size)
    
    def add_entity(self):
        self.bar_down(10)
        self.add_text(text=random.choice(self.israel_supermarkets), x=random.choice([2]), font_size=self.text_size)
    
    def add_summary(self):
        self.bar_down(random.randint(0, self.h // 40))
        base_total_str = "{:.2f}".format(self.total_without_maam)
        self.add_text(text="תשלום ללא מעמ                         " + base_total_str, 
                     x=random.choice([2]), font_size=self.text_size)
        self.bar_down(random.randint(0, self.h // 40))
        final_total = self.total_without_maam * 1.18  # adding 18.0% VAT
        final_total_str = "{:.2f}".format(final_total)
        self.add_text(text="סהכ לתשלום                        " + final_total_str, 
                     x=random.choice([2]), font_size=self.text_size)
    
    def add_dotted_lines_before_table(self):
        self.bar_down(random.randint(0, self.h // 20))
        self.add_text(text=" ".join(["-"] * (self.h // 3)), x=random.choice([2]), font_size=self.text_size)
    
    def add_table(self):
        self.bar_down(random.randint(0, self.h // 10))
        columns = ['קוד', 'תאור', 'כמות']
        xs = [1.15, 2, 10]
        for x, col in zip(xs, columns):
            self.add_text(text=col, x=x, font_size=14)
        self.bar_down()
        for x, col in zip(xs, columns):
            self.add_text(text=(len(col) + 2) * "-", x=x, font_size=14)
        
        product_ids = [get_product_id() for i in range(random.randint(1,8))]
        # Note: There was a reference to product_names which isn't defined in the original code
        # I'm assuming it should be taking names from self.products
        random_products = random.sample(self.products, len(product_ids)) if len(self.products) >= len(product_ids) else self.products
        product_prices = ["{:.2f}".format(random.uniform(1, 10)) for _ in range(len(product_ids))]
        quantities = ["{:.3f}".format(random.randint(1,200) / 100) for _ in range(len(product_ids))]
        
        prod_items = []
        for name, price, quantity in zip(product_ids, product_prices, quantities):
            prod_items.append({"name": name, "price": price, "quantity": quantity})
        
        self.total_without_maam = 0.0  # initialize the sum before VAT
        self.bar_down(random.randint(0, self.h // 20))
        b_down = random.randint(0, self.h // 30)
        
        for product in prod_items:
            row_total = float(product["price"]) * float(product["quantity"])
            self.total_without_maam += row_total
            row_total_str = "{:.2f}".format(row_total)
      
            self.add_text(text=product["name"], x=1.15, font_size=self.text_size)
            self.bar_down(b_down)
            self.add_text(text=f"""X {random.randint(1,100) / 100:.2f} לק"ג""", x=3, font_size=self.text_size)
            self.add_text(text=str(product["quantity"]), x=1.5, font_size=self.text_size)
            self.add_text(text=" ₪" + row_total_str, x=10, font_size=self.text_size)
            self.bar_down(b_down)
    
    def add_domain(self):
        self.bar_down(5)
        self.add_text(text=self.fake.domain_name(), x=random.choice([2]), font_size=self.text_size)
    
    def add_details(self):
        self.bar_down(5)
        self.bar_down(5)
        self.add_text(text=f"טל׳ {get_random_telephone()}", x=random.choice([2]), font_size=self.text_size)
        self.bar_down(5)
        self.add_text(text=f"פקס: {get_random_telephone()}", x=random.choice([2]), font_size=self.text_size)
        self.bar_down(5)
        self.add_text(text=self.fake.address().replace("(", "").replace(")", ""), 
                     x=random.choice([2]), font_size=self.text_size)
        self.bar_down(5)
        self.add_text(text=self.fake.ascii_company_email(), x=random.choice([2]), font_size=self.text_size)
    
    def add_receipt_id(self):
        self.bar_down(5)
        self.add_text(text=random.choice(["קבלה:", "-קב'", "מס' חשבון קבלה", "מספר חשבון", "מס' חשבונית"]), 
                     x=random.choice([1.28]), font_size=self.text_size)
        self.add_text(text=str(random.randint(10000,99999)), x=random.choice([2]), font_size=self.h // 43)
    
    def add_branch(self):
        self.bar_down(7)
        self.add_text(text=random.choice(["סניף:", "-סנ'", ":מס סניף", ":מס' הסניף", "מספר סניף"]), 
                     x=random.choice([1.28]), font_size=self.text_size)
        self.add_text(text=str(random.randint(0,1000)), x=random.choice([2.5]), font_size=self.h // 50)

    def add_checkout(self, bar_down=False):
        if bar_down:
            self.bar_down(7)
        self.add_text(text=random.choice(["קופה:", "-קו'", ":מס קופה", ":מס' הקופה", "מספר קופה"]), 
                     x=random.choice([4]), font_size=self.text_size)
        self.add_text(text=str(random.randint(0,30)), x=random.choice([7]), font_size=self.h // 50)

    def do_nothing(self):
        pass