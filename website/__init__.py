import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'will ciaa'
    
    # Force Flask to use the standard instance folder layout
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(app.instance_path, DB_NAME)}'
    
    db.init_app(app)
    
    # 1. Register Blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    # 2. Import models here to ensure they are registered
    from .models import User, Note, Product  # Make sure Product model is imported here too!

    # 3. Create the database cleanly in the instance folder
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)
        
    with app.app_context():
        db.create_all()
        print('Database synced successfully!')
    
    # 4. Setup Login Manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app