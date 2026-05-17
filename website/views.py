import requests  # Added for making backend calls to Paystack's API
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


# 7. INITIALIZE PAYSTACK CHECKOUT
@views.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash('Your cart is empty!', category='error')
        return redirect(url_for('views.cart'))
        
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    # Paystack processes currency in its smallest unit (Pesewas for GHS). Multiply by 100.
    amount_in_pesewas = int(total * 100)
    
    # Linked to your Starphys Shop Paystack test account profile
    PAYSTACK_SECRET_KEY = "sk_test_159d97b41788508c62d168acf27cd8b7f7d353b7"
    
    url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    
    # Send the user info and local/live callback URL so Paystack returns them to us after paying
    data = {
        "email": current_user.email,
        "amount": amount_in_pesewas,
        "callback_url": "http://127.0.0.1:5000/payment-verify" 
    }
    
    try:
        response = requests.post(url, json=data, headers=headers).json()
        if response.get('status'):
            # Redirect the customer straight to Paystack's hosted payment gateway interface
            return redirect(response['data']['authorization_url'])
        else:
            flash(f"Payment setup failed: {response.get('message')}", category='error')
            return redirect(url_for('views.cart'))
    except Exception as e:
        flash("Unable to connect to the payment processor right now.", category='error')
        return redirect(url_for('views.cart'))


# 8. VERIFY PAYMENT AND CLEAR CART
@views.route('/payment-verify')
@login_required
def payment_verify():
    # Paystack appends a unique ?reference=XYZ query string to the URL when returning
    reference = request.args.get('reference')
    
    if not reference:
        flash('Transaction reference not found.', category='error')
        return redirect(url_for('views.cart'))
        
    PAYSTACK_SECRET_KEY = "sk_test_159d97b41788508c62d168acf27cd8b7f7d353b7"
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}"
    }
    
    try:
        response = requests.get(url, headers=headers).json()
        if response.get('status') and response['data']['status'] == 'success':
            
            # SUCCESS! Clear out all cart items for the user since payment is confirmed
            cart_items = Cart.query.filter_by(user_id=current_user.id).all()
            for item in cart_items:
                db.session.delete(item)
            db.session.commit()
            
            flash('Payment successful! Your custom order has been placed.', category='success')
            return redirect(url_for('views.shop'))
        else:
            flash('Payment verification failed or was cancelled.', category='error')
            return redirect(url_for('views.cart'))
    except Exception as e:
        flash("Error verifying transaction process.", category='error')
        return redirect(url_for('views.cart'))