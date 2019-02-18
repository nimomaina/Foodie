from flask import Flask, render_template
from . import main
import requests
import json
from flask import render_template, request, redirect, url_for, abort, flash
from . import main
from flask_login import login_required, current_user
from ..models import Blog, User, Comment
from .forms import BlogForm, CommentForm,UpdateProfile, UpdateForm
from flask.views import View, MethodView
from .. import db, photos
from datetime import datetime


@main.route("/")
def index():

    return render_template('index.html')


@main.route('/allblogs')
def blog():
    blogs = Blog.query.order_by(Blog.date_posted.desc())
    return render_template('all_blogs.html', blogs=blogs)


@main.route('/blogs/<int:blog_id>',methods = ["GET","POST"])
def view_blog(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()
    random = requests.get('http://quotes.stormconsultancy.co.uk/random.json').json()

    form = CommentForm()
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        new_comment = Comment(name=name, description=description, blog=blog)
        new_comment.save_comment()
        return redirect(url_for('main.view_blog', id=blog.id))
    comments = Comment.query.filter_by(blog_id=blog.id)

    return render_template("blogs.html", blog=blog, comments=comments, random = random)

@main.route('/blogs/new/', methods=['GET', 'POST'])
@login_required
def new_blog():
    form = BlogForm()
    if form.validate_on_submit():
        description = form.description.data
        title = form.title.data
        owner_id = current_user
        date_posted = str(datetime.now())
        print(current_user._get_current_object().id)
        new_blog = Blog(owner_id=current_user._get_current_object().id, title=title, description=description,
                          date_posted=date_posted)
        db.session.add(new_blog)
        db.session.commit()
        flash('New blog post created','success')

        return redirect(url_for('main.blog'))
    return render_template('new_blog.html', form=form)

#
# @main.route('/comment/new/<int:blog_id>', methods=['GET', 'POST'])
# @login_required
# def new_comment(blog_id):
#     form = CommentForm()
#     blog = Blog.query.get(blog_id)
#     if form.validate_on_submit():
#         description = form.description.data
#
#         new_comment = Comment(description=description, user_id=current_user._get_current_object().id, blog_id=blog_id)
#         db.session.add(new_comment)
#         db.session.commit()
#
#         return redirect(url_for('.new_comment', blog_id = blog_id))
#
#     all_comments = Comment.query.filter_by(blog_id=blog_id).all()
#     return render_template('comments.html', form=form, comment=all_comments, blog=blog)
#

@main.route("/delete/<blog_id>",methods = ['GET','POST'])
def delete(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()
    db.session.delete(blog)
    db.session.commit()

    return redirect(url_for('main.blog'))


@main.route("/update/<blog_id>", methods= ['GET', 'POST'])
@login_required
def update_blog(blog_id):
    blog = Blog.query.filter_by(id = blog_id).first()
    form = UpdateForm()
    if form.validate_on_submit():
        blog.title = form.title.data
        blog.description = form.description.data
        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect(url_for('main.blog'))
    elif request.method == 'GET':
        form.title.data = blog.title
        form.description.data = blog.body


    return render_template('new_blog.html', form=form)



@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))