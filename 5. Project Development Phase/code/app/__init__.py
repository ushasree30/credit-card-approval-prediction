import os
from flask import Flask
from app.models import db

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key_12345')
    
    # Database path
    db_path = os.path.join(app.root_path, 'creditcard.db')
    
    # Workaround for Vercel: Copy SQLite DB to /tmp to make it writable
    if os.environ.get('VERCEL') == '1' or os.environ.get('VERCEL_ENV'):
        import shutil
        tmp_db_path = '/tmp/creditcard.db'
        if not os.path.exists(tmp_db_path) and os.path.exists(db_path):
            try:
                shutil.copy2(db_path, tmp_db_path)
            except Exception as e:
                app.logger.error(f"Failed to copy DB to /tmp: {e}")
        db_path = tmp_db_path
        
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    
    # Register Blueprints
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    # Create tables
    with app.app_context():
        db.create_all()
        
    return app
