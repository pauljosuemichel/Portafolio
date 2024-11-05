import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from .models import User
from .forms import LoginForm, RegistrationForm
from flask_login import current_user, login_required, login_user, logout_user
from app import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)  # Aquí se establece la contraseña hasheada
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)


@main.route('/login', methods=['GET', 'POST'])
def login():
    # Si el usuario ya está autenticado, redirigir a la página de inicio
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    
    # Validación del formulario
    if form.validate_on_submit():
        # Buscar al usuario en la base de datos
        user = User.query.filter_by(username=form.username.data).first()
        
        # Verificar si el usuario existe y la contraseña es correcta
        if user and user.check_password(form.password.data):  # Aquí se verifica la contraseña usando el método
            login_user(user)  # Autenticar al usuario
            flash('Has iniciado sesión correctamente.', 'success')
            return redirect(url_for('main.index'))  # Redirigir después del inicio de sesión exitoso
        else:
            flash('Nombre de usuario o contraseña incorrectos.', 'danger')
    
    # Renderizar la plantilla de login
    return render_template('login.html', form=form)

