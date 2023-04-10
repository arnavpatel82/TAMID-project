#this page creates the necessary routes
from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, User
from . import db


views = Blueprint("views", __name__)

#automatically route to the home page when the user logs in
@views.route("/")
@views.route("/home")
@login_required
def home():
    #on the home page, display all posts.
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)



#HTTP request for creating a post
@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        #get values from the form
        title = request.form.get('title')
        text = request.form.get('text')
        tag1 = request.form.get('tag1')
        tag2 = request.form.get('tag2')
        tag3 = request.form.get('tag3')
        isprivate = request.form.get("is_private")
        
        #if values are empty, flash an error message
        if not title or not text or not tag1 or not tag2 or not tag3:
            flash('Posts and tags cannot be empty', category='error')
        else:
            #check the private/public checkbox values
            if isprivate:
                isprivate = 1
            else:
                isprivate = 0
            #create a post with the entered title, text, tags, and update the author and privacy of the post
            post = Post(title=title, text=text, tag1=tag1, tag2=tag2, tag3=tag3, author=current_user.id, is_private=isprivate)
            db.session.add(post)
            db.session.commit()
            #flash a message showing that post has been created, and redirect to the home page.
            flash('Post created!', category='success')
            return redirect(url_for('views.home'))
    #if there is an issue when creating the post, render the create post page.
    return render_template('create_post.html', user=current_user)



#HTTP request for deleting a post
@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    #query for the first post that has the id of the post to be deleted
    post = Post.query.filter_by(id=id).first()
    if not post:
        flash("Post does not exist", category='error')
    elif current_user.id != post.author:
        flash('You do not have permission to delete this post', category='error')
    else:
        #if the post exists and the current logged in user is the author of the post, delete the post, commit changes,
        #and add a flashed message to reflect this
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')
    #no matter what, render the home screen after deletion
    return redirect(url_for('views.home'))



#HTTP request for updating a post
@views.route("/update-post/<id>", methods=['GET', 'POST'])
@login_required
def update_post(id):
    #query for the first post that has the id of the post to be updated
    post = Post.query.filter_by(id=id).first()
    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.author:
        flash('You do not have permission to edit this post.', category='error')
    elif request.method == "POST":
        #if the post exists and the current logged in user is the author, 
        #check to see if the form values are empty
        if not request.form['title'] or not request.form['text'] or not request.form['tag1'] or not request.form['tag2'] or not request.form['tag3']:
            flash('Posts and tags cannot be empty', category='error')
        else:
            #otherwise, update the database table with the new updated values
            post.title = request.form['title']
            post.text = request.form['text']
            post.tag1 = request.form['tag1']
            post.tag2 = request.form['tag2']
            post.tag3 = request.form['tag3']
            #update privacy
            if request.form.get('is_private'):
                post.is_private = 1
            else:
                post.is_private = 0
            db.session.commit()
            #commit changes and redirect to home page
            return redirect(url_for('views.home'))
    #if it fails, render the same update post screen with an error message
    return render_template('update_post.html', post=post, user=current_user)


#HTTP request for viewing a user's posts
@views.route("/posts/<username>")
@login_required
def posts(username):
    #query the database and find the first user with the username that is to be viewed
    user = User.query.filter_by(username=username).first()

    #if user does not exist, flash error message and redirect to home
    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    #query the database and find all posts by the user, based on id
    posts = Post.query.filter_by(author=user.id).all()

    #render the post display screen, with posts = to the queried posts and username of the user to be viewed
    return render_template("posts.html", user=current_user, posts=posts, username=username)



#HTTP request for viewing all posts with the tags equal to tag1
@views.route("/tag1/<tag1>")
@login_required
def tag1_posts(tag1):
    #query for all posts with matching tags to tag1 and display them in posts.html
    posts = Post.query.filter_by(tag1=tag1).all() + Post.query.filter_by(tag2=tag1).all() + Post.query.filter_by(tag3=tag1).all()
    return render_template("posts.html", user=current_user, posts=posts, username=tag1)


#HTTP request for viewing all posts with the tags equal to tag2
@views.route("/tag2/<tag2>")
@login_required
def tag2_posts(tag2):
    #query for all posts with matching tags to tag1 and display them in posts.html
    posts = Post.query.filter_by(tag1=tag2).all() + Post.query.filter_by(tag2=tag2).all() + Post.query.filter_by(tag3=tag2).all()
    return render_template("posts.html", user=current_user, posts=posts, username=tag2)


#HTTP request for viewing all posts with the tags equal to tag3
@views.route("/tag3/<tag3>")
@login_required
def tag3_posts(tag3):
    #query for all posts with matching tags to tag1 and display them in posts.html
    posts = Post.query.filter_by(tag1=tag3).all() + Post.query.filter_by(tag2=tag3).all() + Post.query.filter_by(tag3=tag3).all()
    return render_template("posts.html", user=current_user, posts=posts, username=tag3)


#HTTP request for viewing your private posts
@views.route("<username>/private-posts")
@login_required
def private_posts(username):
    #query the database and find the first user with the username to view
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('no user with that username exists', category='error')
        return redirect(url_for('views.home'))
    
    #query all posts by the user that are private, based on id
    posts = Post.query.filter_by(author=user.id, is_private = 1).all()

    #if there are private posts, render them in posts.html
    if posts:
        return render_template("posts.html", user=current_user, posts=posts, username=username)

    #otherwise, flash that there are no private posts and return to home.html
    else:
        flash('You have no private posts.')
        return render_template("home.html", user=current_user, username=username, posts = Post.query.all())
