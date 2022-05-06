from os import abort
from flask import Flask, render_template, redirect, request, url_for
from flask_login import LoginManager, logout_user, current_user, login_user, login_required
from werkzeug.urls import url_parse
from flask_sqlalchemy import SQLAlchemy

# Own modules
from forms import SignupForm, PostForm, LoginForm

app = Flask(__name__)
# Creamos un token para instancia del formulario 
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:testing@localhost:5432/miniblog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager(app)
login_manager.login_view = "login" # <-- Define la vista que se va a mostrar cuando el usuario no esté logueado
db = SQLAlchemy(app)

# Para que python no ponga problmea de importacion, importamos debajo de de db = SQLAlchemy(app)
from models import User, Post

# Variables
posts = []


#manejo de inicio de sesion
@login_manager.user_loader
def load_user(user_id): #<- es un callback, se puede entender como un middleware 
    return User.get_by_id(int(user_id))


@app.route('/')
def index():
    """Flask busca por defecto las plantillas en la carpeta llamada 'templates' """
    posts = Post.get_all()
    return render_template('index.html', posts=posts)

@app.route('/p/<string:slug>/') #Es buena practica acabar con "/" al final de las rutas. 
def show_post(slug):
    post = Post.get_by_slug(slug)
    if post is None:
        abort(404)
    return render_template('post_view.html', post=post)
    
@app.route("/admin/post/", methods=['GET', 'POST'], defaults={'post_id': None})
@app.route("/admin/post/<int:post_id>/", methods=['GET', 'POST'])
@login_required # <- se protege la vista
def post_form(post_id):
    form = PostForm()
    print(post_id)
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        # title_slug = form.title_slug.data
    
        # Consolidar data y anadir
        post = Post(user_id=current_user.id, title=title, content=content)
        post.save()
        
        return redirect(url_for('index'))
    return render_template("admin/post_form.html", form=form, post_id=post_id)


@app.route("/signup/", methods=['GET', 'POST'])
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

            #Keep new user logged in
            login_user(user, remember=True)

            next_page = request.args.get('next', None)
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template('signup_form.html', form=form, error=error)

@app.route('/login', methods=['GET', 'POST'])
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
                next_page = url_for('index')
            return redirect(next_page)
    return render_template('login_form.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
