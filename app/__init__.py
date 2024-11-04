import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Inicializar las extensiones
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Configuraciones
    app.config['SECRET_KEY'] = 'f5b4c3e7a1f38f841a1fbba779f3acd70e32a3a79c31f8c3'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://ube4fcqrzl0mmiau:SqvA7bBLmB0wHewnFrN5@b0xhxyxbeaxlnhzyfa2m-mysql.services.clever-cloud.com/b0xhxyxbeaxlnhzyfa2m'  # Ajusta según tu configuración
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(app.instance_path, 'uploads')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Inicializar las extensiones
    db.init_app(app)
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
        db.create_all()  # Crear tablas en la base de datos

    return app