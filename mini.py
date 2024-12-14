import base64
from flask import Flask, render_template, request, flash, session, redirect, url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/miniproject?charset=utf8mb4&connect_timeout=10'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.template_filter('b64encode')
def b64encode_filter(data):
    return base64.b64encode(data).decode('utf-8')

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

class Land(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(100), nullable=False)
    acres = db.Column(db.String(100), nullable=False)
    rent = db.Column(db.Integer, nullable=False)
    watersource = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    currentcrop = db.Column(db.String(100), nullable=True)
    facing = db.Column(db.String(100), nullable=True)
    poss = db.Column(db.String(100), nullable=True)
    soil = db.Column(db.String(100), nullable=True)
    owner = db.Column(db.String(100), nullable=False)
    gmail = db.Column(db.String(100), nullable=False)
    properties = db.Column(db.String(100), nullable=True)
    localities = db.Column(db.String(100), nullable=True)
    about = db.Column(db.Text, nullable=True)
    cover_image = db.Column(db.LargeBinary, nullable=True)
    slider_image1 = db.Column(db.LargeBinary, nullable=True)
    slider_image2 = db.Column(db.LargeBinary, nullable=True)
    slider_image3 = db.Column(db.LargeBinary, nullable=True)
    slider_image4 = db.Column(db.LargeBinary, nullable=True)
    slider_image5 = db.Column(db.LargeBinary, nullable=True)


class Equi(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100), nullable=False)
    height=db.Column(db.Integer,nullable=False)
    length=db.Column(db.Integer,nullable=False)
    width=db.Column(db.Integer,nullable=False)
    model=db.Column(db.String(100), nullable=True)
    coo=db.Column(db.String(100), nullable=True)
    weight=db.Column(db.Integer,nullable=False)
    power=db.Column(db.Integer,nullable=False)
    year=db.Column(db.Integer,nullable=False)
    owner_name=db.Column(db.String(100), nullable=False)
    contact_no=db.Column(db.Integer,nullable=False)
    gmail=db.Column(db.String(100), nullable=True)
    equi_listed=db.Column(db.String(100), nullable=True)
    location=db.Column(db.String(100), nullable=True)
    cover_image = db.Column(db.LargeBinary, nullable=False)
    slider_image1 = db.Column(db.LargeBinary, nullable=False)
    slider_image2 = db.Column(db.LargeBinary, nullable=True)
    slider_image3 = db.Column(db.LargeBinary, nullable=True)
    slider_image4 = db.Column(db.LargeBinary, nullable=True)
    slider_image5 = db.Column(db.LargeBinary, nullable=True)

class Product(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    descr=db.Column(db.Text, nullable=True)
    price=db.Column(db.Integer,nullable=False)
    contact_no=db.Column(db.Integer,nullable=False)
    o_name=db.Column(db.String(100), nullable=False)
    mail=db.Column(db.String(100), nullable=True) 
    cover_image = db.Column(db.LargeBinary, nullable=True)
    p_name=db.Column(db.String(100), nullable=False)   
    
class CartItem(db.Model):
    __tablename__ = 'cart_item'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    land_id = db.Column(db.Integer, db.ForeignKey('land.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('cart_items', lazy=True))
    land = db.relationship('Land', backref=db.backref('cart_items', lazy=True))

class EquipmentCartItem(db.Model):
    __tablename__ = 'equipment_cart_item'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equi.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('equipment_cart_items', lazy=True))
    equipment = db.relationship('Equi', backref=db.backref('equipment_cart_items', lazy=True))

class WishlistItem(db.Model):
    __tablename__ = 'wishlist_item'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('wishlist_items', lazy=True))
    product = db.relationship('Product', backref=db.backref('wishlist_items', lazy=True))




@app.route('/')
def home():
    return render_template('/home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            print('email already exists')
            return render_template('/signup.html')
        encpassword = generate_password_hash(password)
        new_user = User(username=username, email=email, password=encpassword)
        db.session.add(new_user)
        db.session.commit()
        print('User created successfully')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and not check_password_hash(user.password, password):
            login_user(user)
            print('correct username')
            return redirect(url_for('land_rental'))
        else:
            print('Invalid username or password.')
    return render_template('login.html')

@app.route('/land_rental')
def land_rental():
    lands = Land.query.all()
    return render_template('landrental.html', lands=lands)

@app.route('/add_land_details', methods=['GET', 'POST'])
@login_required
def add_land_details():
    if request.method == 'POST':
        # Retrieve form data
        lname = request.form.get('lname')
        acres = request.form.get('acres')
        rent = request.form.get('rent')
        watersource = request.form.get('watersource')
        location = request.form.get('location')
        currentcrop = request.form.get('currentcrop')
        facing = request.form.get('facing')
        poss = request.form.get('poss')
        soil = request.form.get('soil')
        owner = request.form.get('owner')
        gmail = request.form.get('gmail')
        properties = request.form.get('properties')
        localities = request.form.get('localities')
        about = request.form.get('about')

        # Process cover image
        cover_image = request.files['cover_image']
        cover_image_data = cover_image.read() if cover_image and allowed_file(cover_image.filename) else None
        
        # Process slider images
        slider_image1 = request.files['slider_image1'].read() if 'slider_image1' in request.files else None
        slider_image2 = request.files['slider_image2'].read() if 'slider_image2' in request.files else None
        slider_image3 = request.files['slider_image3'].read() if 'slider_image3' in request.files else None
        slider_image4 = request.files['slider_image4'].read() if 'slider_image4' in request.files else None
        slider_image5 = request.files['slider_image5'].read() if 'slider_image5' in request.files else None

        # Save data to the database
        new_land = Land(
            lname=lname,
            acres=acres,
            rent=rent,
            watersource=watersource,
            location=location,
            currentcrop=currentcrop,
            facing=facing,
            poss=poss,
            soil=soil,
            owner=owner,
            gmail=gmail,
            properties=properties,
            localities=localities,
            about=about,
            cover_image=cover_image_data,
            slider_image1=slider_image1,
            slider_image2=slider_image2,
            slider_image3=slider_image3,
            slider_image4=slider_image4,
            slider_image5=slider_image5
        )
        db.session.add(new_land)
        db.session.commit()

        flash('Land details added successfully!')
        return redirect(url_for('land_rental'))
    return render_template('add_land_details.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully!', 'success')
    return redirect(url_for('home'))


@app.route('/land_info/<int:land_id>')
def land_info(land_id):
    land = Land.query.get_or_404(land_id)
    return render_template('land_info.html', land=land)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/add_to_cart/<int:land_id>', methods=['POST', 'GET'])
@login_required
def add_to_cart(land_id):
    user_id = current_user.id
    cart_item = CartItem(user_id=user_id, land_id=land_id)
    db.session.add(cart_item)
    db.session.commit()
    flash('Land added to your cart successfully!')
    return redirect(url_for('land_info', land_id=land_id)) 

@app.route('/cart')
@login_required
def cart():
    user_id = current_user.id
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    equipment_cart_items = EquipmentCartItem.query.filter_by(user_id=user_id).all()
    wishlist_items = WishlistItem.query.filter_by(user_id=user_id).all()
    return render_template('cart.html', cart_items=cart_items, equipment_cart_items=equipment_cart_items,wishlist_items=wishlist_items)



@app.route('/remove_from_cart/<int:land_id>', methods=['POST'])
@login_required
def remove_from_cart(land_id):
    user_id = current_user.id
    cart_item = CartItem.query.filter_by(user_id=user_id, land_id=land_id).first()
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        flash('Item removed from your cart successfully!')
    return redirect(url_for('cart'))

@app.route('/equipment_rental')
def equipment_rental():
    equipment = Equi.query.all()
    return render_template('Prental.html', equipment=equipment)

@app.route('/add_equipment_details', methods=['GET', 'POST'])
@login_required
def add_equipment_details():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form.get('name')
        height = request.form.get('height')
        length = request.form.get('length')
        width = request.form.get('width')
        model = request.form.get('model')
        coo = request.form.get('coo')
        weight = request.form.get('weight')
        power = request.form.get('power')
        year = request.form.get('year')
        owner_name = request.form.get('owner_name')
        contact_no = request.form.get('contact_no')
        gmail = request.form.get('gmail')
        equi_listed = request.form.get('equi_listed')
        location = request.form.get('location')

        # Process cover image
        cover_image = request.files['cover_image']
        cover_image_data = cover_image.read() if cover_image and allowed_file(cover_image.filename) else None

        # Process slider images
        slider_image1 = request.files['slider_image1'].read() if 'slider_image1' in request.files else None
        slider_image2 = request.files['slider_image2'].read() if 'slider_image2' in request.files else None
        slider_image3 = request.files['slider_image3'].read() if 'slider_image3' in request.files else None
        slider_image4 = request.files['slider_image4'].read() if 'slider_image4' in request.files else None
        slider_image5 = request.files['slider_image5'].read() if 'slider_image5' in request.files else None

        # Save data to the database
        new_equipment = Equi(
            name=name,
            height=height,
            length=length,
            width=width,
            model=model,
            coo=coo,
            weight=weight,
            power=power,
            year=year,
            owner_name=owner_name,
            contact_no=contact_no,
            gmail=gmail,
            equi_listed=equi_listed,
            location=location,
            cover_image=cover_image_data,
            slider_image1=slider_image1,
            slider_image2=slider_image2,
            slider_image3=slider_image3,
            slider_image4=slider_image4,
            slider_image5=slider_image5
        )
        db.session.add(new_equipment)
        db.session.commit()

        flash('Equipment details added successfully!')
        return redirect(url_for('equipment_rental'))
    return render_template('add_equipment_details.html')

@app.route('/equi_info/<int:equi_id>')
def equi_info(equi_id):
    equip = Equi.query.get_or_404(equi_id)
    return render_template('eq_info.html', equipm=equip)

@app.route('/add_equipment_to_cart/<int:equi_id>', methods=['POST'])
@login_required
def add_equipment_to_cart(equi_id):
    user_id = current_user.id
    equipment_item = EquipmentCartItem(user_id=user_id, equipment_id=equi_id)
    db.session.add(equipment_item)
    db.session.commit()
    flash('Equipment added to your cart successfully!')
    return redirect(url_for('equi_info', equi_id=equi_id))  # Redirect to the equipment page

@app.route('/remove_from_equipment_cart/<int:equi_id>', methods=['POST'])
@login_required
def remove_from_equipment_cart(equi_id):
    user_id = current_user.id
    equipment_item = EquipmentCartItem.query.filter_by(user_id=user_id, equipment_id=equi_id).first()
    if equipment_item:
        db.session.delete(equipment_item)
        db.session.commit()
        flash('Equipment removed from your cart successfully!')
    return redirect(url_for('cart'))  # Redirect back to the cart page

@app.route('/products')
def products():
    products = Product.query.all()  # Fetch all products from the database
    return render_template('product.html', products=products)

@app.route('/add_product_details', methods=['GET', 'POST'])
@login_required
def add_product_details():
    if request.method == 'POST':
        p_name = request.form.get('p_name')
        descr = request.form.get('descr')
        price = request.form.get('price')
        contact_no = request.form.get('contact_no')
        o_name = request.form.get('o_name')
        mail = request.form.get('mail')

        # Process cover image
        cover_image = request.files.get('cover_image')
        if cover_image and allowed_file(cover_image.filename):
            cover_image_data = cover_image.read()
        else:
            flash('Invalid or missing cover image. Please upload a valid image file.')
            return redirect(request.url)

        # Save data to the database
        new_product = Product(
            p_name=p_name,
            descr=descr,
            price=price,
            contact_no=contact_no,
            o_name=o_name,
            mail=mail,
            cover_image=cover_image_data
        )
        db.session.add(new_product)
        db.session.commit()

        flash('Product details added successfully!')
        return redirect(url_for('products'))
    return render_template('add_product_details.html')

@app.route('/add_to_wishlist/<int:product_id>', methods=['POST'])
@login_required
def add_to_wishlist(product_id):
    user_id = current_user.id

    # Check if the product is already in the wishlist
    existing_item = WishlistItem.query.filter_by(user_id=user_id, product_id=product_id).first()
    if existing_item:
        flash('This product is already in your wishlist!')
        return redirect(url_for('products'))  # or wherever you want to redirect after adding

    # Add the product to the wishlist
    wishlist_item = WishlistItem(user_id=user_id, product_id=product_id)
    db.session.add(wishlist_item)
    db.session.commit()

    flash('Product added to your wishlist successfully!')
    return redirect(url_for('products'))


@app.route('/remove_from_wishlist/<int:product_id>', methods=['POST'])
@login_required
def remove_from_wishlist(product_id):
    user_id = current_user.id
    wishlist_item = WishlistItem.query.filter_by(user_id=user_id, product_id=product_id).first()
    if wishlist_item:
        db.session.delete(wishlist_item)
        db.session.commit()
        flash('Product removed from your wishlist successfully!')
    return redirect(url_for('cart'))


@app.route('/filter_lands', methods=['GET'])
def filter_lands():
    acres = request.args.get('acres', type=int)

    if acres:
        lands = Land.query.filter(Land.acres >= acres).all()
    else:
        lands = Land.query.all()

    lands_data = []
    for land in lands:
        land_data = {
            'id': land.id,
            'lname': land.lname,
            'acres': land.acres,
            'location': land.location,
            'watersource': land.watersource,
            'soil': land.soil,
            # Instead of trying to decode the cover_image, base64 encode it
            'cover_image': base64.b64encode(land.cover_image).decode('utf-8') if land.cover_image else None,
        }
        lands_data.append(land_data)

    return jsonify({'lands': lands_data})

@app.route('/forum')
def forum():
    return render_template('forum.html')

if __name__ == "__main__":
    app.run(debug=True)
