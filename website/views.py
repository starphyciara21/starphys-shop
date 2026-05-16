from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Product, Cart 
from . import db

views = Blueprint('views', __name__)

# 1. HOME PAGE
@views.route('/')
def home():
    return render_template("home.html", user=current_user)

# 2. ABOUT PAGE
@views.route('/about')
def about():
    return render_template("about.html", user=current_user)

# 3. SERVICES PAGE
@views.route('/services')
def services():
    return render_template("services.html", user=current_user)

# 4. SHOP PAGE
@views.route('/shop')
def shop():
    # Fetches all products stored in the database to display in the shop
    products = Product.query.all()
    return render_template("shop.html", user=current_user, products=products)

# 5. ADD TO CART (WITH MEASUREMENTS)
@views.route('/add-to-cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    measurements = request.form.get('measurements')
    
    # Checks if this specific item/measurement combination already exists in the user's cart
    cart_item = Cart.query.filter_by(
        user_id=current_user.id, 
        product_id=product_id, 
        custom_notes=measurements
    ).first()

    if cart_item:
        # If it exists, just increase the quantity
        cart_item.quantity += 1
    else:
        # If it's new, create a new Cart entry
        new_item = Cart(
            user_id=current_user.id, 
            product_id=product_id, 
            custom_notes=measurements
        )
        db.session.add(new_item)
    
    db.session.commit()
    flash('Item added with your measurements!', category='success')
    return redirect(url_for('views.shop'))

# 6. CART VIEW
@views.route('/cart')
@login_required
def cart():
    # Retrieve all items currently in the logged-in user's cart
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    
    # Calculate the grand total price based on price and quantity
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    return render_template("cart.html", user=current_user, cart_items=cart_items, total=total)