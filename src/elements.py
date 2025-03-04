import random
from .utils import *

class ReceiptElements:
    """Class for receipt-specific elements"""
    def add_date(self):
        date = get_random_date()
        self.bar_down(random.randint(0, self.h // 100))
        self.add_text(text=date, x=random.choice([100, 2, 1]), font_size=self.text_size)
        self.data.append({"date": date,})
    
    def add_entity(self):
        self.bar_down(10)
        entity = random.choice(self.israel_supermarkets)
        self.add_text(text=entity, x=random.choice([2]), font_size=self.h // 20)
        self.data.append({"entity": entity})

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
        self.data.append({"total_without_maam": base_total_str, "final_total": final_total_str})

    def add_dotted_lines_before_table(self):
        self.bar_down(random.randint(0, self.h // 20))
        self.add_text(text=" ".join(["-"] * (self.h // 3)), x=random.choice([2]), font_size=self.text_size)
    
    def add_table(self):
        self.bar_down(random.randint(0, self.h // 30))
        columns = ['קוד', 'כמות', 'סכום']
        xs = [1.15, 2, 10]
        for x, col in zip(xs, columns):
            self.add_text(text=col, x=x, font_size=14)
        self.bar_down()
        for x, col in zip(xs, columns):
            self.add_text(text=(len(col) + 2) * "-", x=x, font_size=14)
        
        product_ids = [get_product_id() for i in range(random.randint(1,8))]
        random_products = random.sample(self.products, len(product_ids)) if len(self.products) >= len(product_ids) else self.products
        product_prices = ["{:.2f}".format(random.uniform(0, 100) if random.random() > 0.1 else random.uniform(-30, 0)) for _ in range(len(product_ids))]
        quantities = ["{:.3f}".format(random.randint(1,200) / 100) for _ in range(len(product_ids))]
        prod_str_names = random.choices(self.products, k=len(product_ids))
        prod_items = []
        for product_id, name, price, quantity in zip(product_ids, prod_str_names, product_prices, quantities, ):
            prod_dict = {"code": product_id, "name": name, "price": price, "quantity": quantity}
            prod_items.append(prod_dict)

        self.total_without_maam = 0.0  # initialize the sum before VAT
        self.bar_down()
        b_down = random.randint(0, self.h // 80)
        
        for product in prod_items:
            row_total = float(product["price"]) * float(product["quantity"])
            self.total_without_maam += row_total
            row_total_str = "{:.2f}".format(row_total)

            is_weighted_product = random.random() > 0.5
            if is_weighted_product:
                self.add_text(text=product["code"], x=1.15, font_size=self.text_size)
                self.add_text(text=product["name"], x=2.5, font_size=self.text_size)
                self.bar_down(b_down)
                kg_price = random.randint(1,500) / 100
                self.add_text(text=f"""X {kg_price:.2f} לק"ג""", x=3, font_size=self.text_size)
                self.add_text(text=str(product["quantity"]), x=1.5, font_size=self.text_size)
                self.add_text(text=" ₪" + row_total_str, x=10, font_size=self.text_size)
                self.bar_down(b_down)

            else:
                kg_price = None
                product["quantity"] = random.randint(1, 5)
                self.add_text(text=product["code"], x=1.15, font_size=self.text_size)
                self.add_text(text=product["name"], x=3.3, font_size=self.text_size)
                self.add_text(text=str(product["quantity"]), x=2.0, font_size=self.text_size)
                self.add_text(text=" ₪" + row_total_str, x=10, font_size=self.text_size)
                self.bar_down(b_down)

            self.data.append({"code": product["code"], "name": product["name"], "quantity": product["quantity"], "kg_price": kg_price if kg_price is not None else "-", "price_payed": row_total_str})

    
    def add_domain(self):
        self.bar_down(5)
        domain = self.fake.domain_name()
        self.add_text(text=domain, x=random.choice([2]), font_size=self.text_size)
        self.data.append({"domain": domain})
    
    def add_details(self):
        self.bar_down(5)
        self.bar_down(5)

        tl = get_random_telephone()
        self.add_text(text=f"טל׳ {tl}", x=random.choice([2]), font_size=self.text_size)
        self.data.append({"telephone": tl})
        self.bar_down(5)
        
        fax = get_random_telephone()
        self.add_text(text=f"פקס: {fax}", x=random.choice([2]), font_size=self.text_size)
        self.data.append({"fax": fax})

        address = self.fake.address()
        self.bar_down(5)
        self.add_text(text=address.replace("(", "").replace(")", ""), 
                     x=random.choice([2]), font_size=self.text_size)
        self.data.append({"address": address})
        
        email = self.fake.ascii_company_email()
        self.bar_down(5)
        self.add_text(text=email, x=random.choice([2]), font_size=self.text_size)
        self.data.append({"email": email})

    def add_receipt_id(self):
        self.bar_down(5)
        self.add_text(text=random.choice(["קבלה:", "-קב'", "מס' חשבון קבלה", "מספר חשבון", "מס' חשבונית"]), 
                     x=random.choice([1.28]), font_size=self.text_size)
        receipt_id = str(random.randint(10000,99999))
        self.add_text(text=receipt_id, x=random.choice([2]), font_size=self.h // 43)
        self.data.append({"receipt_id": receipt_id})

    def add_branch(self):
        self.bar_down(7)
        branch = random.choice(["סניף:", "-סנ'", ":מס סניף", ":מס' הסניף", "מספר סניף"])
        self.add_text(text=branch, x=1.28, font_size=self.text_size)
        self.add_text(text=str(random.randint(0,1000)), x=random.choice([2.5]), font_size=self.h // 50)
        self.data.append({"branch": branch,})

    def add_checkout(self, bar_down=False):
        if bar_down:
            self.bar_down(7)
        checkout = random.choice(["קופה:", "-קו'", ":מס קופה", ":מס' הקופה", "מספר קופה"])
        self.add_text(text=checkout, x=4, font_size=self.text_size)
        check_out_num = str(random.randint(0,30))
        self.add_text(text=check_out_num, x=random.choice([7]), font_size=self.h // 50)
        self.data.append({"checkout": checkout})
  
    def do_nothing(self):
        pass