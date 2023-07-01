from flask_login import UserMixin


class Staff(UserMixin):
    count = 0
    
    def __init__(self, first_name, last_name, email, mobile_no, password):
        Staff.count += 1
        self.__staff_id = Staff.count
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__mobile_no = mobile_no
        self.__password = password
    
    # set methods
    def set_id(self, id):
        self.__staff_id = id
        
    def set_first_name(self, first_name):
        self.__first_name = first_name
        
    def set_last_name(self, last_name):
        self.__last_name = last_name
        
    def set_email(self, email):
        self.__email = email
        
    def set_mobile_no(self, mobile_no):
        self.__mobile_no = mobile_no
        
    def set_password(self, password):
        self.__password = password
        
    
    # get methods
    def get_id(self):
        return self.__staff_id

    def get_first_name(self):
        return self.__first_name
        
    def get_last_name(self):
        return self.__last_name
        
    def get_email(self):
        return self.__email

    def get_mobile_no(self):
        return self.__mobile_no
        
    def get_password(self):
        return self.__password