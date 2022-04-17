from crypt import methods
from flask import Flask, render_template, redirect, request, url_for


app = Flask(__name__)

# Variables
posts = []


@app.route('/')
def index():
    """Flask busca por defecto las plantillas en la carpeta llamada 'templates' """
    return render_template('index.html', num_posts=len(posts))

@app.route('/p/<string:slug>/') #Es buena practica acabar con "/" al final de las rutas. 
def show_post(slug):
    return render_template('post_view.html', slug_title=slug)
    
@app.route("/admin/post/")
@app.route("/admin/post/<int:post_id>/")
def post_form(post_id=None):
    return render_template('admin/post_form.html', post_id=post_id)

@app.route("/signup/", methods=['GET', 'POST'])
def show_signup_form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        next = request.args.get('next', None)
        if next:
            return redirect(next)
        return redirect(url_for('next'))
    return render_template('signup_form.html')