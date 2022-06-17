from flask import render_template, redirect, url_for, request, current_app
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from app import login_manager
from . import auth_bp
from .forms import SignupForm, LoginForm
from .models import User

from app.common.mail import send_email

@auth_bp.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form =  SignupForm()
    error = None
    if form.validate_on_submit():
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        #Check if email already exists
        user = User.get_by_email(email)
        if user is not None:
            error = f'El email {email} ya esta siendo utilizado'
        else:
            #Create and save new user
            user = User(name=name, email=email)
            user.set_password(password)
            user.save()

            # Send email with confirmation welcome message
            send_email(
                subject='Bienvenido al miniblog de camilo',
                sender=current_app.config['DONT_REPLY_FROM_EMAIL'],
                recipients=[email, ],
                text_body=f'Hola {name}, bienvenid@ al miniblog de Flask ---',
                # html_body=f'<p>Hola <strong>{name}</strong>, Te saluda Julian, bienvenido a este blog</p>'
                )

            #Keep new user logged in
            login_user(user, remember=True)

            next_page = request.args.get('next', None)
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('public.index')
            return redirect(next_page)
    return render_template('auth/signup_form.html', form=form, error=error)


@auth_bp.route('/login/', methods=['GET', 'POST'])
def login():
    # current_user viene desde flask_login
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('public.index')
            return redirect(next_page)
    return render_template('auth/login_form.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('public.index'))

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))
