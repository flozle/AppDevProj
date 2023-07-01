from classes.Staff import Staff


class Admin(Staff):
    count = 0
    
    def __init__(self, first_name, last_name, email, mobile_no, password):
        super().__init__(first_name, last_name, email, mobile_no, password)
        Admin.count += 1
        self.__admin_id = Admin.count
        self.__id = f"admin_{Admin.count}"
        
    # set methods
    def set_admin_id(self, id):
        self.__admin_id = id
        
    
    # get methods
    def get_admin_id(self):
        return self.__admin_id
    
    def get_id(self):
        return self.__id
    
    
    def __str__(self):
        return f"id: {self.get_admin_id()}, first name: {self.get_first_name()}, last name: {self.get_last_name()}, email:{self.get_email()}, mobile_no:{self.get_mobile_no()}, password:{self.get_password()}"