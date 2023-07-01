from flask_login import UserMixin


class User(UserMixin):
    count = 0
    
    def __init__(self, email, mobile_no, password):
        User.count += 1
        self.__id = f"user_{User.count}"
        self.__user_id = User.count
        self.__email = email
        self.__mobile_no = mobile_no
        self.__password = password
        self.__cart = []
    
    # set methods
    def set_id(self, id):
        self.__user_id = id
    
    def set_email(self, email):
        self.__email = email
        
    def set_mobile_no(self, mobile_no):
        self.__mobile_no = mobile_no
    
    def set_password(self, password):
        self.__password = password

    def set_cart(self,cart):
        self.__cart = cart
        
    
    # get methods
    def get_id(self):
        return self.__id
    
    def get_user_id(self):
        return self.__user_id
        
    def get_email(self):
        return self.__email
    
    def get_mobile_no(self):
        return self.__mobile_no
    
    def get_password(self):
        return self.__password

    def get_cart(self):
        return self.__cart
    
    
    def __str__(self):
        return f"id: {self.get_user_id()}, email:{self.get_email()}, mobile_no:{self.get_mobile_no()}, password:{self.get_password()}, cart:{self.get_cart()}"
    