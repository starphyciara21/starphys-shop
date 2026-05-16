from website import create_app, db
from website.models import Product

app = create_app()

with app.app_context():
    # Add a few starter products
    item1 = Product(
        name="Business Strategy Session", 
        price=150.00, 
        description="A 1-hour deep dive into your business model.",
        image_url="https://via.placeholder.com/150"
    )
    item2 = Product(
        name="Starter Web Package", 
        price=500.00, 
        description="A 3-page marketing website for your brand.",
        image_url="https://via.placeholder.com/150"
    )
    
    db.session.add(item1)
    db.session.add(item2)
    db.session.commit()
    print("Database seeded with products!")# -*- coding: utf-8 -*-

