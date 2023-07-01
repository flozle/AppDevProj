class Product:
    count_id = 0

    def __init__(self, name, price, image, description, discount=0):
        Product.count_id += 1
        self.__product_name = name
        self.__price = price
        self.__image = image
        self.__description = description
        self.__discount = discount

    def get_name(self):
        return self.__product_name

    def get_price(self):
        return self.__price

    def get_image(self):
        return self.__image

    def get_description(self):
        return self.__description

    def get_discount(self):
        return self.__discount

    def set_name(self, name):
        self.__product_name = name

    def set_price(self, price):
        self.__price = price

    def set_image(self, image):
        self.__image = image

    def set_description(self, description):
        self.__description = description

    def set_discount(self, discount):
        self.__discount = discount

class Cart_Product(Product):
    def __init__(self, name, price, image, description, discount, count):
        super().__init__(name, price, image, description, discount)
        self.__count = 1
        self.__unique_id = name + str(price) + description

    def set_count(self,count):
        self.__count = count

    def get_count(self):
        return self.__count

    def get_unique_id(self):
        return self.__unique_id

    def __str__(self):
        return self.__unique_id



