from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import UserMixin, current_user
from . import login_manager


class Quote:
    '''
    Quote class to define random quotes
    '''

    def __init__(self, quote):
        self.quote = quote

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, index=True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
    blog = db.relationship('Blog', backref='user', lazy='dynamic')
    comment = db.relationship('Comment', backref='user', lazy='dynamic')
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)

    def __repr__(self):
        return f'{self.username}'


class Blog(db.Model):
    '''
    '''
    __tablename__ = 'blogs'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.String(), index=True)
    title = db.Column(db.String())
    category = db.Column(db.String(255), nullable=False)
    comments = db.relationship('Comment', backref='pitch', lazy='dynamic')
    @classmethod
    def get_blogs(cls, id):
        blogs = Blog.query.order_by(blog_id=id).desc().all()
        return Blog

    def __repr__(self):
        return f'Blog {self.description}'


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('pitches.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return f"Comment : id: {self.id} comment: {self.description}"

