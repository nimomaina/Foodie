from flask import Flask, render_template
from . import main
import requests
import json
from flask import render_template, request, redirect, url_for, abort, flash
from . import main
from flask_login import login_required, current_user
from ..models import Blog, User, Comment
from .forms import PitchForm, CommentForm, UpvoteForm, UpdateProfile
from flask.views import View, MethodView
from .. import db, photos



@main.route("/")
def index():
    r = requests.get('http://quotes.stormconsultancy.co.uk/random.json')
    quote = r['quote']
    return render_template('index.html', quote=quote)



@main.route('/pickup', methods=['GET', 'POST'])
def pickup():
    pitch = Pitch.query.filter_by().first()
    pickuppitch = Pitch.query.filter_by(category="pickuppitch")
    return render_template('pick-up.html', pitch=pitch, pickuppitch=pickuppitch)

@main.route('/business', methods=['GET', 'POST'])
def business():
    pitch = Pitch.query.filter_by().first()
    businesspitch= Pitch.query.filter_by(category="businesspitch")

    return render_template('business.html', businesspitch=businesspitch, pitch=pitch)

@main.route('/interview', methods=['GET', 'POST'])
def interview():
    pitch = Pitch.query.filter_by().first()
    interviewpitch = Pitch.query.filter_by(category="interviewpitch")

    return render_template('interview.html', pitch=pitch, interviewpitch=interviewpitch)

@main.route('/technology', methods=['GET', 'POST'])
def technology():
    techpitch = Pitch.query.filter_by(category="techpitch")
    pitch = Pitch.query.filter_by().first()
    return render_template('technology.html', pitch=pitch, techpitch=techpitch)

@main.route('/pitches/new/', methods=['GET', 'POST'])
@login_required
def new_pitch():
    form = PitchForm()
    my_upvotes = Upvote.query.filter_by(pitch_id=Pitch.id)
    if form.validate_on_submit():
        description = form.description.data
        title = form.title.data
        owner_id = current_user
        category = form.category.data
        print(current_user._get_current_object().id)
        new_pitch = Pitch(owner_id=current_user._get_current_object().id, title=title, description=description,
                          category=category)
        db.session.add(new_pitch)
        db.session.commit()

        return redirect(url_for('main.index'))
    return render_template('pitches.html', form=form)


@main.route('/comment/new/<int:pitch_id>', methods=['GET', 'POST'])
@login_required
def new_comment(pitch_id):
    form = CommentForm()
    pitch = Pitch.query.get(pitch_id)
    if form.validate_on_submit():
        description = form.description.data

        new_comment = Comment(description=description, user_id=current_user._get_current_object().id, pitch_id=pitch_id)
        db.session.add(new_comment)
        db.session.commit()

        return redirect(url_for('.new_comment', pitch_id=pitch_id))

    all_comments = Comment.query.filter_by(pitch_id=pitch_id).all()
    return render_template('comments.html', form=form, comment=all_comments, pitch=pitch)

