from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv
import os

# Carga las variables de entorno
load_dotenv()

# Configuración de la aplicación Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_RECYCLE'] = 280
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_pre_ping': True}

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

# Formularios de WTF Flask
class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

# Decorador para verificar si el usuario está autenticado
def login_required(f):
    def wrap(*args, **kwargs):
        if 'username' not in session:
            flash('Inicia sesión para acceder.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrap

# Ruta para manejar el inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['username'] = user.username
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('inicio'))
        flash('Credenciales incorrectas. Inténtalo nuevamente.', 'danger')
    return render_template('login.html', form=form)

# Ruta de cierre de sesión
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    flash('Sesión cerrada.', 'info')
    return redirect(url_for('login'))

# Rutas restringidas
@app.route('/')
def inicio():
    is_authenticated = 'user_id' in session  # Ajusta según cómo guardes el estado de autenticación
    return render_template('base.html', is_authenticated=is_authenticated)



# Creación de tablas en la base de datos si no existen
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)