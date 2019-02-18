from flask import Flask, render_template
from . import main
import requests
import json
from flask import render_template, request, redirect, url_for, abort, flash
from . import main
from flask_login import login_required, current_user
from ..models import Blog, User, Comment
from .forms import BlogForm, CommentForm,UpdateProfile
from flask.views import View, MethodView
from .. import db



@main.route("/")
def index():
    r = requests.get('http://quotes.stormconsultancy.co.uk/random.json')
    quote = r['quote']
    return render_template('index.html', quote=quote)



@main.route('/food', methods=['GET', 'POST'])
def foodie():
    blog = Blog.query.filter_by().first()
    foodie = Blog.query.filter_by(category="foodie")
    random = requests.get('http://quotes.stormconsultancy.co.uk/random.json').json()

    return render_template('food.html', blog=blog, foodie=foodie, random=random)

@main.route('/style', methods=['GET', 'POST'])
def style():
    blog = Blog.query.filter_by().first()
    style= Blog.query.filter_by(category="style")
    random = requests.get('http://quotes.stormconsultancy.co.uk/random.json').json()
    return render_template('style.html', style=style, blog=blog, random=random)

@main.route('/techie', methods=['GET', 'POST'])
def technology():
    techie = Blog.query.filter_by(category="techie")
    blog = Blog.query.filter_by().first()
    random = requests.get('http://quotes.stormconsultancy.co.uk/random.json').json()
    return render_template('technology.html', blog=blog, techie=techie, random=random)

@main.route('/blogs/new/', methods=['GET', 'POST'])
@login_required
def new_blog():
    form = BlogForm()
    if form.validate_on_submit():
        description = form.description.data
        title = form.title.data
        owner_id = current_user
        category = form.category.data
        print(current_user._get_current_object().id)
        new_blog = Blog(owner_id=current_user._get_current_object().id, title=title, description=description,
                          category=category)
        db.session.add(new_blog)
        db.session.commit()

        return redirect(url_for('main.index'))
    return render_template('blogs.html', form=form)


@main.route('/comment/new/<int:blog_id>', methods=['GET', 'POST'])
@login_required
def new_comment(blog_id):
    form = CommentForm()
    blog = Blog.query.get(blog_id)
    if form.validate_on_submit():
        description = form.description.data

        new_comment = Comment(description=description, user_id=current_user._get_current_object().id, blog_id=blog_id)
        db.session.add(new_comment)
        db.session.commit()

        return redirect(url_for('.new_comment', blog_id = blog_id))

    all_comments = Comment.query.filter_by(blog_id=blog_id).all()
    return render_template('comments.html', form=form, comment=all_comments, blog=blog)

