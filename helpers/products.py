class AllProducts():
    def __init__(self, tg_dolar, all_products):
        self.tg_dolar = tg_dolar
        self.all_products = all_products
    
    def get_all_product(self):
        products = {
            "tg_dolar": self.tg_dolar,
            "products": self.all_products
        }
        return products
        
class MainProduct():
    def __init__(self, prod_pn: float, prod_in_tg: bool, tg_product, inf_product, prod_need_udpate: bool):
        self.prod_pn = prod_pn
        self.prod_in_tg = prod_in_tg
        self.tg_product = tg_product
        self.infosep_product = inf_product
        self.prod_need_udpate = prod_need_udpate

    def get_product(self):
        product = {
            "prod_pn": self.prod_pn,
            "prod_in_tg": self.prod_in_tg,
            "prod_need_update": self.prod_need_udpate,
            "tg": self.tg_product.get_product(),
            "infosep": self.infosep_product.get_product()
        }
        return product

class Product:
    def __init__(self, id: str, name: str, desc: str, categories: list, price: float, brand: str, stock: int, images: list):
        self.id = id
        self.name = name
        self.desc = desc
        self.categories = categories
        self.price = price
        self.brand = brand
        self.stock = stock
        self.images = images

    def get_product(self):
        product = {
            "id": self.id,
            "name": self.name,
            "desc": self.desc,
            "cat": self.categories,
            "price": self.price,
            "brand": self.brand,
            "stock": self.stock,
            "images": self.images
        }
        return product
    
class InfosepProduct(Product):
    def __init__(self, id: str, name: str, desc: str, categories: list, price: float, brand: str, stock: int, images: list, infosep_id: int, reg_price: int, sale_price: int, status: str, update: bool):
        super().__init__(id, name, desc, categories, price, brand, stock, images)
        self.infosep_id = infosep_id
        self.reg_price = reg_price
        self.sale_price = sale_price
        self.status = status
        self.update = update

    def get_product(self):
        n_product = super().get_product()
        n_product["infosep_id"] = self.infosep_id
        n_product["price"] = self.empty_string_to_zero(self.price)
        n_product["reg_price"] = self.empty_string_to_zero(self.reg_price)
        n_product["sale_price"] = self.empty_string_to_zero(self.sale_price)
        n_product["status"] = self.status
        n_product["update"] = self.update
        return n_product
    
    def empty_string_to_zero(self, field):
        if field == '':
            field = 0
        return int(field)

class TecnoGlobalProduct(Product):
    def __init__(self, id: str = "", name: str = "", desc: str = "", categories: list = None, price: float = 0.0, brand: str = "", stock: int = 0, images: list = None, code: str = ""):
        if categories is None:
            categories = []
        if images is None:
            images = []

        super().__init__(id, name, desc, categories, price, brand, stock, images)
        self.code = code

    def get_product(self):
        n_product = super().get_product()
        n_product["code"] = self.code
        return n_product