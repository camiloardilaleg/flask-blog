from crypt import methods
from email.mime import image
import logging

from app.auth.decorators import admin_required
from app.auth.models import User
from app.models import Post
from flask import abort, redirect, render_template, request, url_for, current_app
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import os

from . import admin_bp
from .forms import PostForm, UserAdminForm

from werkzeug.utils import secure_filename
import os

logger = logging.getLogger(__name__)


@admin_bp.route("/admin/")
@login_required
@admin_required
def index():
    return render_template("admin/index.html")

@admin_bp.route("/admin/post/", methods=['GET', 'POST'], defaults={'post_id': None})
@admin_required # Only admin can access this route
@login_required # Only logged users can access this route
def post_form(post_id):
    """Crea un nuevo post"""
    form = PostForm()
    if form.validate_on_submit(): # only when form is submitted by Post method
        title = form.title.data
        content = form.content.data
        file = form.post_image.data
        image_name = None

        # Check if file is in request
        if file:
            image_name = secure_filename(file.filename)
            images_dir = current_app.config['POSTS_IMAGES_DIR']
            os.makedirs(images_dir, exist_ok=True)
            file_path = os.path.join(images_dir, image_name)
            file.save(file_path)

        post = Post(user_id=current_user.id, title=title, content=content)
        post.image_name = image_name
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

### ---- USERS ---- ###
# List all users
@admin_bp.route('/admin/users')
@login_required
@admin_required
def list_users():
    users = User.get_all()
    return render_template("admin/users.html", users=users)

@admin_bp.route('/admin/user/<int:user_id>/', methods=['GET', 'POST'])
@login_required
@admin_required
def update_user_form(user_id):
    user = User.get_by_id(user_id)
    if user is None:
        logger.info(f'El usuario {user_id} no existe')
        abort(404)
    form = UserAdminForm(obj=user)
    if form.validate_on_submit():
        # Actualiza los campos del usuario existente
        user.is_admin = form.is_admin.data
        user.save()
        logger.info(f'Guardando el usuario {user_id}')
        return redirect(url_for('admin.list_users'))
    return render_template("admin/user_form.html", form=form, user=user)

@admin_bp.route("/admin/user/delete/<int:user_id>/", methods=['POST', ])
@login_required
@admin_required
def delete_user(user_id):
    logger.info(f'Se va a eliminar al usuario {user_id}')
    user = User.get_by_id(user_id)
    if user is None:
        logger.info(f'El usuario {user_id} no existe')
        abort(404)
    user.delete()
    logger.info(f'El usuario {user_id} ha sido eliminado')
    return redirect(url_for('admin.list_users'))