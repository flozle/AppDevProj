from classes.Staff import Staff


class Trainer(Staff):
    count = 0
    
    def __init__(self, first_name, last_name, email, mobile_no, password):
        super().__init__(first_name, last_name, email, mobile_no, password)
        Trainer.count += 1
        self.__id = f"trainer_{Trainer.count}"
        self.__trainer_id = Trainer.count
        
    # set methods
    def set_trainer_id(self, id):
        self.__trainer_id = id
        
    
    # get methods
    def get_id(self):
        return self.__id
    
    def get_trainer_id(self):
        return self.__trainer_id
    
    
    def __str__(self):
        return f"id: {self.get_trainer_id()}, first name: {self.get_first_name()}, last name: {self.get_last_name()}, email:{self.get_email()}, mobile_no:{self.get_mobile_no()}, password:{self.get_password()}"