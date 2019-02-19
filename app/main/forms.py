from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,SubmitField,TextAreaField,RadioField, SelectField
from wtforms.validators import Required,Email,EqualTo
from wtforms import ValidationError

class BlogForm(FlaskForm):
    title = StringField('Title for you Blog')
    description = TextAreaField('Blog Content')
    submit = SubmitField('Publish')

class CommentForm(FlaskForm):
    name = StringField('Name',validators=[Required()])
    description = TextAreaField('Add comment',validators=[Required()])
    submit = SubmitField()

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Fill in the bio info', validators=[Required()])
    submit = SubmitField('Submit')

class UpdateForm(FlaskForm):
    title = StringField('Title for you Blog',validators=[Required()])
    description = TextAreaField('Blog Content',validators=[Required()])
    submit = SubmitField('Edit')