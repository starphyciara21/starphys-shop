# -*- coding: utf-8 -*-

import os
from website import create_app, db
from website.models import Product

app = create_app()

# FORCE BOTH THE SCRIPT AND WEB APP TO USE THE WEBSITE PACKAGE DATABASE
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(base_dir, "website", "instance", "database.db")}'

def add_starphys_products():
    with app.app_context():
        # 1. Clear out previous structural logs completely
        print("Wiping old database entries...")
        db.drop_all()
        db.create_all()
        db.session.commit() 

        # 2. Complete clean catalog matching your exact renamed files
        products = [
            # --- Apparel ---
            Product(name="Signature Mesh Top", price=35.00, image_url="/static/images/mesh.jpg"),
            Product(name="Crochet Mini Skirt", price=45.00, image_url="/static/images/ladys_skirt.jpg"),
            Product(name="Men's Mesh Shirt", price=60.00, image_url="/static/images/mens_shirt.jpg"),
            Product(name="Custom Summer Shorts", price=60.00, image_url="/static/images/mens_shorts.jpg"),
            Product(name="Handmade Cardigan (Style 1)", price=100.00, image_url="/static/images/kadigan1.jpg"),
            Product(name="Handmade Cardigan (Style 2)", price=100.00, image_url="/static/images/kadigan2.jpg"),
            Product(name="Menswear Crochet Top", price=75.00, image_url="/static/images/menswear1.jpg"),

            # --- Bags ---
            Product(name="Boho Crochet Bag (Pastel)", price=65.00, image_url="/static/images/bag1.jpg"),
            Product(name="Luxury Earth-Tone Handbag", price=65.00, image_url="/static/images/bag2.jpg"),
            Product(name="Cozy Shoulder Bag (Brown)", price=65.00, image_url="/static/images/bag3.jpg"),
            Product(name="Structured Knit Handbag", price=180.00, image_url="/static/images/bag4.jpg"),
            Product(name="Elegant White Sling Bag", price=180.00, image_url="/static/images/bag5.jpg"),
            Product(name="Classic Black Statement Bag", price=180.00, image_url="/static/images/bag6.jpg"),
            Product(name="Sunburst Textured Tote", price=65.00, image_url="/static/images/bag7.jpg"),

            # --- Bonnets & Beanies ---
            Product(name="Classic Knit Beanie", price=30.00, image_url="/static/images/beanie.jpg"),
            Product(name="Satin-Lined Bonnet (Purple)", price=80.00, image_url="/static/images/bonnet.jpg"),
            Product(name="Cozy Bonnet (Pink)", price=80.00, image_url="/static/images/bonnet1.jpg"),
            Product(name="Warm Winter Bonnet", price=80.00, image_url="/static/images/bonnet3.jpg"),
            Product(name="Premium Chunky Bonnet", price=80.00, image_url="/static/images/bonnet6.jpg"),

            # --- Mesh Hats ---
            Product(name="Signature Mesh Hat", price=30.00, image_url="/static/images/mesh_hat.jpg"),
            Product(name="Mesh Hat (Style 1)", price=30.00, image_url="/static/images/mesh_hat1.jpg"),
            Product(name="Mesh Hat (Style 2)", price=30.00, image_url="/static/images/mesh_hat2.jpg"),
            Product(name="Mesh Hat (Style 3)", price=30.00, image_url="/static/images/mesh_hat3.jpg"),
            Product(name="Mesh Hat (Style 4)", price=30.00, image_url="/static/images/mesh_hat4.jpg"),
            Product(name="Mesh Hat (Style 5)", price=30.00, image_url="/static/images/mesh_hat5.jpg"),
            Product(name="Mesh Hat (Style 6)", price=30.00, image_url="/static/images/mesh_hat6.jpg"),
            Product(name="Mesh Hat (Style 7)", price=30.00, image_url="/static/images/mesh_hat7.jpg"),
            Product(name="Mesh Hat (Style 8)", price=30.00, image_url="/static/images/mesh_hat8.jpg"),
            Product(name="Mesh Hat (Style 9)", price=30.00, image_url="/static/images/mesh_hat9.jpg"),
            Product(name="Mesh Hat (Style 10)", price=30.00, image_url="/static/images/mesh_hat10.jpg"),
            Product(name="Mesh Hat (Style 11)", price=30.00, image_url="/static/images/mesh_hat11.jpg"),
            Product(name="Mesh Hat (Style 12)", price=30.00, image_url="/static/images/mesh_hat12.jpg"),
            Product(name="Mesh Hat (Style 13)", price=30.00, image_url="/static/images/mesh_hat13.jpg"),

            # --- Raffle Hats & Bands ---
            Product(name="Raffle Band", price=35.00, image_url="/static/images/raffle_band.jpg"),
            Product(name="Raffle Statement Hat (Gold)", price=85.00, image_url="/static/images/raffle_hat.jpg"),
            Product(name="Boho Raffle Hat (Cream)", price=85.00, image_url="/static/images/raffle_hat1.jpg"),
            Product(name="Vintage Ruffle Hat", price=85.00, image_url="/static/images/raffle_hat2.jpg"),
            Product(name="Sun-Protection Raffle Hat", price=85.00, image_url="/static/images/raffle_hat4.jpg"),
            Product(name="Statement Raffle Hat", price=85.00, image_url="/static/images/raffle_hat7.jpg"),
            Product(name="Autumn Raffle Hat", price=85.00, image_url="/static/images/raffle_hat8.jpg"),
            Product(name="Flouncy Ruffle Hat", price=85.00, image_url="/static/images/raffle_hat6.jpg"),

            # --- Scrunchies ---
            Product(name="Velvet Crochet Scrunchie (Red Pack)", price=25.00, image_url="/static/images/scrunchie1.jpg"),
            Product(name="Cloud-Soft Pastel Scrunchie", price=25.00, image_url="/static/images/scrunchie2.jpg"),
            Product(name="Stacked Statement Scrunchie", price=25.00, image_url="/static/images/scrunchie4.jpg"),
            Product(name="Multi-Color Mega Scrunchie Pack", price=25.00, image_url="/static/images/scrunchie5.jpg")
        ]

        db.session.add_all(products)
        db.session.commit()
        print(f"Successfully loaded {len(products)} Starphys products into the correct database!")

if __name__ == "__main__":
    add_starphys_products()