from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,SubmitField,TextAreaField,RadioField, SelectField
from wtforms.validators import Required,Email,EqualTo
from wtforms import ValidationError

class BlogForm(FlaskForm):
    title = StringField('Title for you Blog')
    description = TextAreaField(' ')
    submit = SubmitField('New Blog Post')

class CommentForm(FlaskForm):
    name = StringField('Enter your name',validators=[Required()])
    description = TextAreaField('Add comment',validators=[Required()])
    submit = SubmitField()

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.', validators=[Required()])
    submit = SubmitField('Submit')

class UpdateForm(FlaskForm):
    title = StringField('Title for you Blog',validators=[Required()])
    description = TextAreaField(' ',validators=[Required()])
    submit = SubmitField('Edit')