from flask import abort, render_template, current_app
from app.models import Post
from . import public_bp

from werkzeug.exceptions import NotFound
import logging

logger = logging.getLogger(__name__)

@public_bp.route("/")
def index():
    # the logger is defined in the app.__init__.py
    current_app.logger.info("Showing post's blog")
    logger.info('Mostrando los post del log')
    posts = Post.get_all()
    return render_template("public/index.html", posts=posts)


@public_bp.route("/p/<string:slug>/")
def show_post(slug):
    
    # Logs section
    logger.info('Mostrando un pos especifico')
    logger.debug(f'Mostrando el post con slug {slug}')
    
    post = Post.get_by_slug(slug)
    if post is None:
        raise NotFound(slug)
    return render_template("public/post_view.html", post=post)

@public_bp.route("/error")
def show_error():
    res = 1/0
    posts = Post.get_all()
    return render_template("public/index.html", posts=posts)

"""
current_app.logger.info("Showing post's blog")
logger.info('Mostrando los post del log')

Ambas opciones envian logs, pero la segunda se crea una instancia en el modulo que queramos, y es un poco 
mas especifica, la cual es fundamental al momento de debuggear eficientemente.
"""