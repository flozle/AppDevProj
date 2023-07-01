import contextlib
from wtforms import Form, validators, ValidationError, StringField, PasswordField, SelectField, BooleanField, Field, TextAreaField, DecimalField, FileField, IntegerField
from wtforms.widgets import TextInput, PasswordInput
from wtforms.fields import EmailField, DateField
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
import classes.Admin as Admin
import shelve


class PhoneField(Field):
    widget = TextInput()
    pass


# ==================================custom validators================================================
# check if field is int
def validate_mobile_no(form, field):
    try:
        int(field.data)
    except ValueError as e:
        raise ValidationError('Mobile No must only consist of numbers') from e

# check if passwords are the same
def validate_confirm_password(form, field):
    if form.password.data != field.data:
        raise ValidationError("Your passwords does not match")

# ===============================================================================================
# check if the email is taken already
def validate_email_checker(form, field):
    user_dict = {}
    admins_dict = {}
    trainers_dict = {}
    dbs = shelve.open('staff.db', 'c')
    dbu = shelve.open('user.db', 'c')
    
    # open dictornary in shelve
    try:
        user_dict = dbu['Users']
    except Exception:
        print("Error in retrieving User from user.db")
        
    try:
        admins_dict = dbs['Admins']
    except Exception:
        print("Error in retriveing Admin from staff.db")
        
    try:
        trainers_dict = dbs['Trainers']
    except Exception:
        print("Error in retriveing Trainer from staff.db")
        
    dbu.close()
    dbs.close()
    
    for dicts in [user_dict, admins_dict, trainers_dict]:
        for email in dicts.values():
            if field.data == email.get_email():
                with contextlib.suppress(Exception):
                    if field.data == form.old_email.data:
                        return
                raise ValidationError("The email address has already been used")

# check if the mobile number is taken already
def validate_mobile_no_checker(form, field):
    user_dict = {}
    admins_dict = {}
    trainers_dict = {}
    dbs = shelve.open('staff.db', 'c')
    dbu = shelve.open('user.db', 'c')

    # open dictornary in shelve
    try:
        user_dict = dbu['Users']
    except Exception:
        print("Error in retrieving User from user.db")

    try:
        admins_dict = dbs['Admins']
    except Exception:
        print("Error in retriveing Admin from staff.db")

    try:
        trainers_dict = dbs['Trainers']
    except Exception:
        print("Error in retriveing Trainer from staff.db")

    dbu.close()
    dbs.close()

    for dicts in user_dict, admins_dict, trainers_dict:
        for mobile_no in dicts.values():
            if field.data ==  mobile_no.get_mobile_no():
                with contextlib.suppress(Exception):
                    if field.data == form.old_mobile_no.data:
                        return
                raise ValidationError("The mobile number has already been used")

# ===============================================================================================
# check if its a exsisting account
def validate_login(form, field):
    user_dict = {}
    admins_dict = {}
    trainers_dict = {}
    dbs = shelve.open('staff.db', 'c')
    dbu = shelve.open('user.db', 'c')

    # open dictionary in shelve
    try:
        user_dict = dbu['Users']
    except Exception:
        print("Error in retrieving User from user.db")

    try:
        admins_dict = dbs['Admins']
    except Exception:
        print("Error in retriveing Admin from staff.db")

    try:
        trainers_dict = dbs['Trainers']
    except Exception:
        print("Error in retriveing Trainer from staff.db")

    dbu.close()
    dbs.close()
    
    for dict in [user_dict, admins_dict, trainers_dict]:
        for user in dict.values():
            if field.data in [user.get_email(), user.get_mobile_no()]:
                if form.password.data == user.get_password():
                    form.session.data = user
                    return
                else:
                    raise ValidationError("Invalid password")
    raise ValidationError("Account not found")


class CreateUserForm(Form):
    email = EmailField('Email', [validators.Email(), validate_email_checker, validators.DataRequired()])
    mobile_no = StringField('Phone', [validate_mobile_no_checker, validate_mobile_no, validators.length(min=8, max=8), validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()], id='password')
    confirm_password = PasswordField('Confirm Password', [validate_confirm_password, validators.DataRequired()], id='confirm_password')

class CreateStaffForm(Form):
    first_name = StringField('First Name', [validators.DataRequired()])
    last_name = StringField('Last Name', [validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validate_email_checker, validators.DataRequired()])
    mobile_no = StringField('Phone', [validators.length(min=8, max=8), validate_mobile_no, validate_mobile_no_checker, validators.DataRequired()])
    role = SelectField('Role', choices=[('', 'Select'), ('T', 'Trainers'), ('A', 'Administrator')], default='')
    password = PasswordField('Password', [validators.DataRequired()])

class CreateLoginForm(Form):
    email_mobile_no = StringField('', [validate_login, validators.DataRequired()])
    password = PasswordField('', [validators.DataRequired()])
    session = StringField()

class UpdateUserForm(Form):
    old_email = EmailField()
    old_mobile_no = StringField()
    email = EmailField('Email', [validators.Email(), validate_email_checker, validators.DataRequired()])
    mobile_no = StringField('Phone', [validate_mobile_no, validate_mobile_no_checker, validators.length(min=8, max=8), validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()], id='password')
    confirm_password = PasswordField('Confirm Password', [validate_confirm_password, validators.DataRequired()], id='confirm_password')
    
class UpdateStaffForm(Form):
    old_email = EmailField()
    old_mobile_no = StringField()
    first_name = StringField('First Name', [validators.DataRequired()])
    last_name = StringField('Last Name', [validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validate_email_checker, validators.DataRequired()])
    mobile_no = StringField('Phone', [validators.length(min=8, max=8), validate_mobile_no, validators.DataRequired()])
    role = SelectField('Role', choices=[('', 'Select'), ('T', 'Trainers'), ('A', 'Administrator')], default='')
    password = PasswordField('Password', [validators.DataRequired()])

class CreateProductForm(Form):
    name = StringField('Item Name', [validators.DataRequired() ,validators.Length(min=1, max=50), validators.DataRequired()])
    price = DecimalField('Item Price', [validators.DataRequired(), validators.number_range(1.00,100.00,message="Please enter a number between 1 to 100")])
    discount = StringField('Item Discount', [validators.DataRequired(), validators.Length(min=1, max=100), validators.DataRequired()])
    description = TextAreaField('Item Description', [validators.DataRequired(), validators.Length(min=1, max=150), validators.DataRequired()])

class ProductQuantityForm(Form):
    product_quantity = IntegerField('Item Qty', [validators.DataRequired(), validators.number_range(1,10,message="Please enter a number between 1 to 10")])

class FileUploadForm(FlaskForm):
    image = FileField('image', validators=[FileRequired()])