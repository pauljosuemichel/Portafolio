import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Inicializar las extensiones
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Configuraciones
    # app.config['SECRET_KEY'] = 'R4geyTIgCFsA209p9gw'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://uao9waaukjmabbi1:R4geyTIgCFsA209p9gw@b5enkloxuwfxrkmyr6km-mysql.services.clever-cloud.com/b5enkloxuwfxrkmyr6km'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(app.instance_path, 'uploads')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Inicializar las extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Cargar las rutas
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Inicializar la base de datos
    with app.app_context():
        db.create_all() 
    return app