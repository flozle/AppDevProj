from flask import Flask, render_template, request, redirect, url_for
from flask_uploads import configure_uploads, IMAGES, UploadSet
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from Forms import CreateUserForm, CreateStaffForm, CreateLoginForm, UpdateUserForm, UpdateStaffForm, CreateProductForm, FileUploadForm, ProductQuantityForm
import classes.User as User, classes.Trainer as Trainer, classes.Admin as Admin, classes.Shop as Shop
import shelve
# kaiser test :D


app = Flask(__name__, static_url_path='/static')

# app initialization
app.secret_key = 'xxxxyyyyyzzzzz'
app.config['SECRET_KEY'] = 'test'
app.config['UPLOADED_IMAGES_DEST'] = 'static/uploads/images'
images = UploadSet('images', IMAGES)
configure_uploads(app, images)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# create user trainer and admin when not found (base)
def create_new_trainer():
    db = shelve.open('staff.db', 'c')
    Trainer.Trainer.count = 0
    trainers_dict = {
        1: Trainer.Trainer(
            'trainer', 'trainer', 'trainer@gmail.com', '11111111', 'trainer'
        )
    }
    db['Trainer_count'] = Trainer.Trainer.count
    db['Trainers'] = trainers_dict
    print('hi')
    return

def create_new_admin():
    db = shelve.open('staff.db', 'c')
    Admin.Admin.count = 0
    admins_dict = {
        1: Admin.Admin(
            'admin', 'admin', 'admin@gmail.com', '22222222', 'admin'
        )
    }
    db['Admin_count'] = Admin.Admin.count
    db['Admins'] = admins_dict
    return

def create_new_user():
    db = shelve.open('user.db', 'c')
    User.User.count = 0
    users_dict = {
        1: User.User('user@gmail.com', '00000000', 'user')
    }
    db['User_count'] = User.User.count
    db['Users'] = users_dict
    return


# home page
@app.route('/')
def home():  # sourcery skip: avoid-builtin-shadow
    email = ""
    id = ""
    # test code
    print(current_user)
    try:
        email = current_user.get_email()
        id = current_user.get_id()
    except Exception:
        print ('unknown user')
    return render_template('home.html', email = email, id = id)

# ===============================================================================================
# Create User
@app.route('/create_user', methods=['GET', 'POST'])
def create_users():
    create_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        user_dict = {}
        db = shelve.open('user.db', 'c')
    
        # open dictornary in shelve
        try:
            user_dict = db['Users']
            User.User.count = db['Count']
        except Exception:
            print("Error in retrieving User from user.db")


        user = User.User(create_user_form.email.data, create_user_form.mobile_no.data, create_user_form.password.data)
        user_dict[user.get_user_id()] = user
        db['Users'] = user_dict
        db['Count'] = user.count
        
        # test code
        for key, item in user_dict.items():
            print(f"{key},{item}")
        
        db.close()
        return redirect(url_for('home'))
        
        
    return render_template('CreateUserPage.html', form=create_user_form)
        

# create staff
@app.route('/create_staff', methods=['GET', 'POST'])
def create_staff():
    create_staff_form = CreateStaffForm(request.form)
    if request.method == 'POST' and create_staff_form.validate():
        admins_dict = {}
        trainers_dict = {}
        db = shelve.open('staff.db', 'c')

        # open dictornary in shelve and update count
        try:
            trainers_dict = db['Trainers']
            Trainer.Trainer.count = db['Trainer_count']
        except Exception:
            create_new_trainer()
            print("Error in retrieving Trainer from staff.db")
        
        try:
            admins_dict = db['Admins']
            Admin.Admin.count = db['Admin_count']
        except Exception:
            create_new_admin()
            print("Error in retrieving Trainer from staff.db")


        if (create_staff_form.role.data) == 'T':
            trainer = Trainer.Trainer(create_staff_form.first_name.data,
                                      create_staff_form.last_name.data,
                                      create_staff_form.email.data,
                                      create_staff_form.mobile_no.data,
                                      create_staff_form.password.data)
            trainers_dict[trainer.get_trainer_id()] = trainer
            db['Trainers'] = trainers_dict
            db['Trainer_count'] = trainer.count
            return redirect(url_for('home'))

        elif (create_staff_form.role.data) == 'A':
            admin = Admin.Admin(create_staff_form.first_name.data,
                                create_staff_form.last_name.data,
                                create_staff_form.email.data,
                                create_staff_form.mobile_no.data,
                                create_staff_form.password.data)
            admins_dict[admin.get_admin_id()] = admin
            db['Admins'] = admins_dict
            db['Admin_count'] = admin.count
            return redirect(url_for('home'))

        db.close()
        
        # test code
        for key, item in trainers_dict.items():
            print(f"{key},{item}")
        for key, item in admins_dict.items():
            print(f"{key},{item}")
            

    return render_template('CreateStaffPage.html', form=create_staff_form)


# ===============================================================================================
# login & logout
@login_manager.user_loader
def load_user(user_id):
    users_dict = {}
    admins_dict = {}
    trainers_dict = {}
    dbs = shelve.open('staff.db', 'c')
    dbu = shelve.open('user.db', 'c')

    # open dictornary in shelve
    try:
        users_dict = dbu['Users']
    except Exception:
        create_new_user()
        print("Error in retrieving User from user.db")

    try:
        admins_dict = dbs['Admins']
    except Exception:
        create_new_admin()
        print("Error in retriveing Admin from staff.db")

    try:
        trainers_dict = dbs['Trainers']
    except Exception:
        create_new_trainer()
        print("Error in retriveing Trainer from staff.db")

    dbu.close()
    dbs.close()

    try:
        for dicts in [users_dict, admins_dict, trainers_dict]:
            for user in dicts.values():
                if user_id == user.get_id():
                    return user
    except Exception:
        print('user not found in db')


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = CreateLoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        login_user(login_form.session.data)

        # test code
        print(login_form.session.data)
        
        return redirect(url_for('home'))
    return render_template('LoginPage.html', form=login_form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


# ===============================================================================================
# user account management (personal)
@app.route('/manage_account')
@login_required
def manage_account():
    role_id = ""
    try:
        role_id = current_user.get_id()
    except Exception:
        print ('unknown user')
        return redirect(url_for('home'))
    role = role_id.split('_')[0]
    print(role)
    if role == "user":
        return redirect(url_for('manage_account_user'))
    elif role == "admin":
        return redirect(url_for('manage_account_admin'))
    elif role == "trainer":
        return redirect(url_for('manage_account_trainer'))
    # test code (error prevention)
    return redirect(url_for('home'))


@app.route('/manage_account_user')
def manage_account_user():
    update_user_form = UpdateUserForm(request.form)
    return render_template('ManageAccountUserPage.html', form=update_user_form)


@app.route('/manage_account_admin')
def manage_account_admin():
    pass


@app.route('/manage_account_trainer')
def manage_account_trainer():
    pass


# ===============================================================================================
# user account management (staff only pages)
@app.route('/retrieve_user')
@login_required
def retrieve_users():  # sourcery skip: avoid-builtin-shadow
    role_id = ""
    try:
        role_id = current_user.get_id()
    except Exception:
        print ('unknown user')
    role_id.split('_')
    role = role_id.split('_')[0]
    id = role_id.split('_')[1]
    print(role)
    if role != "admin":
        return redirect(url_for('no_access'))
    users_dict = {}
    db = shelve.open('user.db', 'c')
    try:
        users_dict = db['Users']
    except Exception:
        create_new_user()
        print("Error in retrieving User from user.db")

    db.close()

    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)

    return render_template('RetrieveUserPage.html', count=len(users_list), users_list=users_list)


@app.route('/update_user/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    update_user_form = UpdateUserForm(request.form)
    users_dict = {}
    if request.method == 'POST' and update_user_form.validate():
        db = shelve.open('user.db', 'w')
        users_dict = db['Users']
        user = users_dict.get(id)

        
        user.set_email(update_user_form.email.data)
        user.set_mobile_no(update_user_form.mobile_no.data)
        user.set_password(update_user_form.password.data)

        db['Users'] = users_dict
        db.close()
        return redirect(url_for('retrieve_users'))
    else:
        db = shelve.open('user.db', 'r')
        users_dict = db['Users']
        db.close()
        user = users_dict.get(id)
        update_user_form.email.data = user.get_email()
        update_user_form.mobile_no.data = user.get_mobile_no()
        update_user_form.old_email.data = user.get_email()
        update_user_form.old_mobile_no.data = user.get_mobile_no()
        return render_template('UpdateUserPage.html', form=update_user_form)


@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    users_dict = {}
    db = shelve.open('user.db', 'w')
    users_dict = db['Users']
    users_dict.pop(id)
    db['Users'] = users_dict
    db.close()
    return redirect(url_for('retrieve_users'))


# ===============================================================================================
# staff account management (staff only pages)
@app.route('/retrieve_staff')
def retrieve_staffs():
    db = shelve.open('staff.db', 'c')
    try:
        trainers_dict = db['Trainers']
    except Exception:
        trainers_dict = {}
    try:
        admins_dict = db['Admins']
    except Exception:
        admins_dict = {}
    db.close()

    trainers_list = []
    admins_list = []
    trainers_list.extend(trainers_dict.get(key) for key in trainers_dict)
    admins_list.extend(admins_dict.get(key) for key in admins_dict)
    return render_template('RetrieveStaffPage.html', trainer_count = len(trainers_list), admin_count = len(admins_list), admins_list = admins_list, trainers_list = trainers_list)


@app.route('/update_staff/<int:id>/<role>', methods=['GET', 'POST'])
def update_staff(id, role):
    update_staff_form = UpdateStaffForm  (request.form)
    trainers_dict = {}
    admins_dict = {}
    if request.method == 'POST' and update_staff_form.validate():
        db = shelve.open('staff.db', 'w')
        trainers_dict = db['Trainers']
        admins_dict = db['Admins']

        # no change in roles
        if update_staff_form.role.data == role == 'A':
            staff = admins_dict.get(id)
            staff.set_first_name(update_staff_form.first_name.data)
            staff.set_last_name(update_staff_form.last_name.data)
            staff.set_email(update_staff_form.email.data)
            staff.set_mobile_no(update_staff_form.mobile_no.data)
            staff.set_password(update_staff_form.password.data)
            
        elif update_staff_form.role.data == role == 'T':
            staff = trainers_dict.get(id)
            staff.set_first_name(update_staff_form.first_name.data)
            staff.set_last_name(update_staff_form.last_name.data)
            staff.set_email(update_staff_form.email.data)
            staff.set_mobile_no(update_staff_form.mobile_no.data)
            staff.set_password(update_staff_form.password.data)
        
        # change in roles
        elif update_staff_form.role.data == 'T':
            Trainer.Trainer.count = len(trainers_dict)
            trainer = Trainer.Trainer(update_staff_form.first_name.data,
                                      update_staff_form.last_name.data,
                                      update_staff_form.email.data,
                                      update_staff_form.mobile_no.data,
                                      update_staff_form.password.data)
            trainers_dict[trainer.get_trainer_id()] = trainer
            admins_dict.pop(id)
            
        elif (update_staff_form.role.data) == 'A':
            Admin.Admin.count = len(admins_dict)
            admin = Admin.Admin(update_staff_form.first_name.data,
                                update_staff_form.last_name.data,
                                update_staff_form.email.data,
                                update_staff_form.mobile_no.data,
                                update_staff_form.password.data)
            admins_dict[admin.get_admin_id()] = admin
            trainers_dict.pop(id)
        else:
            print("why are you here")
        
        db['Admins'] = admins_dict
        db['Trainers'] = trainers_dict
        db.close()
        return redirect(url_for('retrieve_staffs'))
    else:
        db = shelve.open('staff.db', 'r')
        trainers_dict = db['Trainers']
        admins_dict = db['Admins']
        if role == 'A':
            staff = admins_dict.get(id)
            update_staff_form.first_name.data = staff.get_first_name()
            update_staff_form.last_name.data = staff.get_last_name()
            update_staff_form.email.data = staff.get_email()
            update_staff_form.mobile_no.data = staff.get_mobile_no()
            update_staff_form.role.data = role
            update_staff_form.password.data = staff.get_password()
            update_staff_form.old_email.data = staff.get_email()
            update_staff_form.old_mobile_no.data = staff.get_mobile_no()
            
        elif role == 'T':
            staff = trainers_dict.get(id)
            update_staff_form.first_name.data = staff.get_first_name()
            update_staff_form.last_name.data = staff.get_last_name()
            update_staff_form.email.data = staff.get_email()
            update_staff_form.mobile_no.data = staff.get_mobile_no()
            update_staff_form.role.data = role
            update_staff_form.password.data = staff.get_password()
            update_staff_form.old_email.data = staff.get_email()
            update_staff_form.old_mobile_no.data = staff.get_mobile_no()
        
        return render_template('UpdateStaffPage.html', form = update_staff_form)


@app.route('/delete_trainer/<int:id>', methods=['POST'])
def delete_trainer(id):
    trainers_dict = {}
    db = shelve.open('staff.db', 'w')
    trainers_dict = db['Trainers']
    trainers_dict.pop(id)
    db['Trainers'] = trainers_dict
    db.close()
    return redirect(url_for('retrieve_staffs'))


@app.route('/delete_admin/<int:id>', methods=['POST'])
def delete_admin(id):
    admins_dict = {}
    db = shelve.open('staff.db', 'w')
    admins_dict = db['Admins']
    admins_dict.pop(id)
    db['Admins'] = admins_dict
    db.close()
    return redirect(url_for('retrieve_staffs'))


# ===============================================================================================
# staff product management (staff only pages)
@app.route("/manage_shop", methods=['GET', 'POST'])
def manage_shop():

    try:
        shop_list = []
        shop_db = shelve.open('shop.db', "c")

        if 'Product' in shop_db:
            shop_list = shop_db["Product"]
        else:
            shop_db["Product"] = shop_list

    except IOError:
        print("Error opening shop db")



    # Create product creation form
    create_product_form = CreateProductForm(request.form)
    file_upload_form = FileUploadForm()

    if file_upload_form.validate_on_submit():
        image = images.save(file_upload_form.image.data)


    # When submit button clicked
    if request.method == 'POST':
        name = create_product_form.name.data
        price = create_product_form.price.data
        discount = create_product_form.discount.data
        description = create_product_form.description.data

        product = Shop.Product(name, price, image, description, discount)
        shop_list.append(product)
        shop_db['Product'] = shop_list

        shop_db.close()


    return render_template("ManageShopPage.html", shop_list=shop_list, form=create_product_form,fileform=file_upload_form)


@app.route('/updateProduct/<int:id>/', methods=['GET','POST'])
def update_product(id):
    update_product_form = CreateProductForm(request.form)
    if request.method == "POST" and update_product_form.validate():
        shop_list = []
        db = shelve.open('shop.db','w')
        shop_list = db['Product']

        product = shop_list[id]
        product.set_name(update_product_form.name.data)
        product.set_price(update_product_form.price.data)
        product.set_discount(update_product_form.discount.data)
        product.set_description(update_product_form.description.data)
        product.set_image_path(update_product_form.image.data)

        db['Product'] = shop_list
        db.close()

        return redirect(url_for('manage_shop'))
    else:
        product_list = []
        db = shelve.open('shop.db','r')
        product_list = db['Product']
        db.close()

        product = product_list[id]
        update_product_form.name.data = product.get_name()
        update_product_form.price.data = product.get_price()
        update_product_form.discount.data = product.get_discount()
        update_product_form.description.data = product.get_description()
        update_product_form.image.data = product.get_image_path()

        return render_template('updateProduct.html', form=update_product_form)



@app.route('/deleteProduct/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    shop_list = []
    shop_db = shelve.open('shop.db', "w")
    shop_list = shop_db["Product"]

    shop_list.pop(product_id)
    shop_db['Product'] = shop_list
    shop_db.close()

    return redirect(url_for('manage_shop'))


# ===============================================================================================
@app.route('/shop')
def shop():
    try:
        shop_list = []
        shop_db = shelve.open('shop.db', "c")

        if 'Product' in shop_db:
            shop_list = shop_db["Product"]
        else:
            shop_db["Product"] = shop_list
    except IOError:
        print("Error opening shop db")

    size = len(shop_list)

    return render_template('Shop.html', shop_list=shop_list, shop_list_size=len(shop_list), size=size)


# ===============================================================================================
# Product page{{ key.get_count() }}
@app.route('/shop_product/<int:product_id>', methods=['POST'])
def shop_product(product_id):
    try:
        shop_list = []
        shop_db = shelve.open('shop.db', "c")

        if 'Product' in shop_db:
            shop_list = shop_db["Product"]
        else:
            shop_db["Product"] = shop_list
    except IOError:
        print("Error opening shop db")

    # Product variable for rendering
    product = shop_list[product_id]
    product_image = product.get_image()

    #create form
    qty_form = ProductQuantityForm(request.form)
    if request.method == "POST" and qty_form.validate():
        print("test")



    return render_template('ShopProduct.html', product=product, product_image=product_image, qty_form=qty_form)


# ===============================================================================================
# Cart Page
@app.route('/cart')
def cart():
    #get the user's cart
    user_cart = current_user.get_cart()

    #handle calculations here
    subtotal = 0
    for product_kvp in user_cart:
        for product in product_kvp:
            quantity = product_kvp[product]
            price = product.get_price()
            subtotal += (quantity * price)

    total = subtotal

    return render_template('Cart.html',user_cart=user_cart, subtotal=subtotal, total = total)

# ===============================================================================================
# Add To Cart Function
@app.route('/add_to_cart/<int:product_id>/<int:qty>', methods=['POST','GET'])
def add_to_cart(product_id, qty):
    #open shop db
    shop_list = []
    shop_db = shelve.open('shop.db', "c")
    shop_list = shop_db["Product"]

    #open user db
    user_dict = {}
    user_db = shelve.open('user.db','c')
    user_dict = user_db['Users']

    #set current user
    user_id = current_user.get_user_id()
    user = user_dict[user_id]

    #add to cart
    user_cart = user.get_cart()
    shop_item = shop_list[product_id]
    cart_item = Shop.Cart_Product(shop_item.get_name(),shop_item.get_price(),shop_item.get_image(),shop_item.get_description(),shop_item.get_discount(), 1)

    #algorithm

    similar = False
    for product in user_cart:
        for key in product:
            if key.get_unique_id() == cart_item.get_unique_id():
                new_count = key.get_count() + 1
                key.set_count(new_count)
                item = {key:key.get_count()}
                index = user_cart.index(product)
                similar = True
                break

    if similar:
        user_cart[index] = item
    else:
        item = {cart_item: cart_item.get_count()}
        user_cart.append(item)

    #save
    user_dict[user.get_user_id()] = user
    user_db['Users'] = user_dict

    return redirect(url_for('shop'))


# ===============================================================================================
# Cart Page
@app.route('/remove_from_cart/<int:item_index>' ,methods=['POST'])
def remove_from_cart(item_index):
    #open user db
    user_dict = {}
    user_db = shelve.open('user.db','c')
    user_dict = user_db['Users']

    #set current user
    user_id = current_user.get_user_id()
    user = user_dict[user_id]

    #remove from cart
    user_cart = user.get_cart()
    user_cart.pop(item_index)

    # save
    user.set_cart(user_cart)
    user_dict[user.get_user_id()] = user
    user_db['Users'] = user_dict

    return redirect(url_for('cart'))


# ===============================================================================================
# error pages
@app.route('/no_access')
def no_access():  # sourcery skip: avoid-builtin-shadow
    email = ""
    id = ""
    # test code
    print(current_user)
    try:
        email = current_user.get_email()
        id = current_user.get_id()
    except Exception:
        print('unknown user')
    return render_template("NoAccessPage.html", email = email, id = id)


# ===============================================================================================
# LAST LINE (run the website)
@app.route('/test')
def test():
    return render_template('test.html')


# ===============================================================================================
# LAST LINE (run the website)
if __name__ == '__main__':
    app.run()
