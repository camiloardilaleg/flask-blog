from flask import Flask, render_template, redirect, request, url_for
from flask_login import LoginManager, logout_user, current_user, login_user, login_required
from werkzeug.urls import url_parse

# Own modules
from forms import SignupForm, PostForm, LoginForm
from models import users, get_user, User

app = Flask(__name__)
# Creamos un token para instancia del formulario 
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
login_manager = LoginManager(app)
login_manager.login_view = "login" # <-- Define la vista que se va a mostrar cuando el usuario no esté logueado


# Variables
posts = []


#manejo de inicio de sesion
@login_manager.user_loader
def load_user(user_id): #<- es un callback, se puede entender como un middleware 
    for user in users:
        if user.id == int(user_id):
            return user
    return None


@app.route('/')
def index():
    """Flask busca por defecto las plantillas en la carpeta llamada 'templates' """
    return render_template('index.html', posts=posts)

@app.route('/p/<string:slug>/') #Es buena practica acabar con "/" al final de las rutas. 
def show_post(slug):
    return render_template('post_view.html', slug_title=slug)
    
@app.route("/admin/post/", methods=['GET', 'POST'], defaults={'post_id': None})
@app.route("/admin/post/<int:post_id>/", methods=['GET', 'POST'])
@login_required # <- se protege la vista
def post_form(post_id):
    form = PostForm()
    print(post_id)
    if form.validate_on_submit():
        title = form.title.data
        title_slug = form.title_slug.data
        content = form.content.data
    
        # Consolidar data y anadir
        post = {'title': title, 'title_slug': title_slug, 'content': content}
        posts.append(post)
        
        return redirect(url_for('index'))
    return render_template("admin/post_form.html", form=form, post_id=post_id)


@app.route("/signup/", methods=['GET', 'POST'])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form =  SignupForm()
    if form.validate_on_submit():
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        #Create and save new user
        user = User(len(users) + 1, name, email, password)
        users.append(user)

        #Keep new user logged in
        login_user(user, remember=True)

        next_page = request.args.get('next', None)
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('signup_form.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # current_user viene desde flask_login
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user(form.email.data)
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
