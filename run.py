from flask import Flask, render_template

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