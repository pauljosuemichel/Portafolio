from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la aplicación Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialización de la base de datos
db = SQLAlchemy(app)

# Modelo de usuario
class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    es_admin = db.Column(db.Boolean, default=False)

# Crear o actualizar el usuario
with app.app_context():
    # Cambiar las credenciales según sea necesario
    username = 'admin'
    plain_password = '1234'
    email = 'admin@gmail.com'
    es_admin = True

    # Verificar si el usuario ya existe
    user = Usuario.query.filter_by(username=username).first()
    if user:
        # Actualizar la contraseña
        user.password = generate_password_hash(plain_password, method='pbkdf2:sha256')
        db.session.commit()
        print("Contraseña del usuario admin actualizada.")
    else:
        # Crear un nuevo usuario
        hashed_password = generate_password_hash(plain_password, method='pbkdf2:sha256')
        new_user = Usuario(username=username, password=hashed_password, email=email, es_admin=es_admin)
        db.session.add(new_user)
        db.session.commit()
        print("Nuevo usuario admin creado.")
