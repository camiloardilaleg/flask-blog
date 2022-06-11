from flask import abort
from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from app.models import Post
from . import admin_bp
from .forms import PostForm

from app.auth.decorators import admin_required
import logging

logger = logging.getLogger(__name__)

@admin_bp.route("/admin/post/", methods=['GET', 'POST'], defaults={'post_id': None})
@admin_required # Only admin can access this route
@login_required # Only logged users can access this route
def post_form(post_id):
    """Crea un nuevo post"""
    form = PostForm()
    if form.validate_on_submit(): # only when form is submitted by Post method
        title = form.title.data
        content = form.content.data

        post = Post(user_id=current_user.id, title=title, content=content)
        post.save()

        logger.info(f'Saving a new post: {title}')
        return redirect(url_for('public.index'))
    return render_template("admin/post_form.html", form=form)

@admin_bp.route("/admin/post/<int:post_id>/", methods=['GET', 'POST'])
@login_required
@admin_required
def update_post_form(post_id):
    """Actualiza un post"""
    post = Post.get_by_id(post_id)

    if post is None:
        logger.info(f'the post with id {post_id} does not exist')
        abort(404)
    
    # load data from saved post in order to update
    form = PostForm(obj=post)
    if form.validate_on_submit():
        # update post
        post.title = form.title.data
        post.content = form.content.data
        post.save()
        
        logger.info(f'Updating post: {post.title}')
        return redirect(url_for('admin.list_posts'))
    return render_template("admin/post_form.html", form=form, post=post)

# Delete post
@admin_bp.route("/admin/post/delete/<int:post_id>/", methods=['POST', ])
@login_required
@admin_required
def delete_post(post_id):
    logger.info(f'Se va a eliminar el post {post_id}')
    post = Post.get_by_id(post_id)
    if post is None:
        logger.info(f'El post {post_id} no existe')
        abort(404)
    post.delete()
    logger.info(f'El post {post_id} ha sido eliminado')
    return redirect(url_for('admin.list_posts'))

# list all posts
@admin_bp.route("/admin/posts/")
@login_required
@admin_required
def list_posts():
    posts = Post.get_all()
    return render_template("admin/list_posts.html", posts=posts)