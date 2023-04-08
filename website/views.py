#this page creates the necessary routes
from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, User
from . import db


views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)


@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        title = request.form.get('title')
        text = request.form.get('text')
        tag1 = request.form.get('tag1')
        tag2 = request.form.get('tag2')
        tag3 = request.form.get('tag3')
        isprivate = request.form.get("is_private")
        


        if not title or not text or not tag1 or not tag2 or not tag3:
            flash('Posts and tags cannot be empty', category='error')
        else:
            if isprivate:
                isprivate = 1
            else:
                isprivate = 0
            post = Post(title=title, text=text, tag1=tag1, tag2=tag2, tag3=tag3, author=current_user.id, is_private=isprivate)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('create_post.html', user=current_user)


@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    if not post:
        flash("Post does not exist", category='error')
    elif current_user.id != post.author:
        flash('You do not have permission to delete this post', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')
    return redirect(url_for('views.home'))


@views.route("/update-post/<id>", methods=['GET', 'POST'])
@login_required
def update_post(id):
    post = Post.query.filter_by(id=id).first()
    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.author:
        flash('You do not have permission to edit this post.', category='error')
    elif request.method == "POST":
        if not request.form['title'] or not request.form['text'] or not request.form['tag1'] or not request.form['tag2'] or not request.form['tag3']:
            flash('Posts and tags cannot be empty', category='error')
        else:
            post.title = request.form['title']
            post.text = request.form['text']
            post.tag1 = request.form['tag1']
            post.tag2 = request.form['tag2']
            post.tag3 = request.form['tag3']
            db.session.commit()
            return redirect(url_for('views.home'))

    return render_template('update_post.html', post=post, user=current_user)


@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))
    posts = Post.query.filter_by(author=user.id).all()

    return render_template("posts.html", user=current_user, posts=posts, username=username)

@views.route("/tag1/<tag1>")
@login_required
def tag1_posts(tag1):
    posts = Post.query.filter_by(tag1=tag1).all()

    return render_template("posts.html", user=current_user, posts=posts, username=tag1)

@views.route("/tag2/<tag2>")
@login_required
def tag2_posts(tag2):
    posts = Post.query.filter_by(tag2=tag2).all()

    return render_template("posts.html", user=current_user, posts=posts, username=tag2)

@views.route("/tag3/<tag3>")
@login_required
def tag3_posts(tag3):
    posts = Post.query.filter_by(tag3=tag3).all()

    return render_template("posts.html", user=current_user, posts=posts, username=tag3)

@views.route("<username>/private-posts")
@login_required
def private_posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('no user with that username exists', category='error')
        return redirect(url_for('views.home'))
    posts = Post.query.filter_by(author=user.id, is_private = 1).all()

    if posts:
        return render_template("posts.html", user=current_user, posts=posts, username=username)
    else:
        flash('You have no private posts.')
        return render_template("home.html", user=current_user, username=username, posts = Post.query.all())
