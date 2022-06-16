from crypt import methods
from flask import abort, redirect, render_template, current_app, redirect, request, url_for
from app.models import Post, Comment
from . import public_bp

from werkzeug.exceptions import NotFound
import logging
from app.public.forms import CommentForm
from flask_login import current_user


logger = logging.getLogger(__name__)

@public_bp.route("/")
def index():
    # the logger is defined in the app.__init__.py
    current_app.logger.info("Showing post's blog")
    logger.info('Mostrando los post del log')
    page = int(request.args.get('page', 1)) # Obtenemos el numero de pagina que el usuario desea
    items_per_page = current_app.config['ITEMS_PER_PAGE'] # Obtenemos el numero de items por pagina desde variables de la app
    post_pagination = Post.all_paginated(page, items_per_page) # si no tengo mas de tres no muestra nada
    return render_template("public/index.html", post_pagination=post_pagination)


@public_bp.route("/p/<string:slug>/", methods=["GET", "POST"])
def show_post(slug):
    
    # Logs section
    logger.info('Mostrando un pos especifico')
    logger.debug(f'Mostrando el post con slug {slug}')
    
    post = Post.get_by_slug(slug)
    if post is None:
        raise NotFound(slug)

    form = CommentForm()
    if current_user.is_authenticated and form.validate_on_submit():
        content = form.content.data
        comment = Comment(content=content, 
                          user_id=current_user.id, 
                          user_name=current_user.name, 
                          post_id=post.id)
        comment.save()
        return redirect(url_for('public.show_post', slug=post.title_slug))

    return render_template("public/post_view.html", post=post, form=form)

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