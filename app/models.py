from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import db, login_manager, app
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    profession = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    user_id = db.Column(db.Integer, nullable=False, default='None')
    # image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # doctor = db.relationship('Doctor', backref='author', lazy=True)

    # def get_reset_token(self, expires_sec=1800):
    #     s = Serializer(app.config['SECRET_KEY'], expires_sec)
    #     return s.dumps({'user_id': self.id}).decode('utf-8')

    # @staticmethod
    # def verify_reset_token(token):
    #     s = Serializer(app.config['SECRET_KEY'])
    #     try:
    #         user_id = s.loads(token)['user_id']
    #     except:
    #         return None
    #     return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

# @login_manager.user_loader
# def load_doctor(user_id):
#     return Doctor.query.get(int(user_id))

# class Doctor(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     profession = db.Column(db.String(20), nullable=False, default = 'Doctor')
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, default='None')
#     # image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
#     password = db.Column(db.String(60), nullable=False)
#     # posts = db.relationship('Post', backref='author', lazy=True)

#     # def get_reset_token(self, expires_sec=1800):
#     #     s = Serializer(app.config['SECRET_KEY'], expires_sec)
#     #     return s.dumps({'user_id': self.id}).decode('utf-8')

#     # @staticmethod
#     # def verify_reset_token(token):
#     #     s = Serializer(app.config['SECRET_KEY'])
#     #     try:
#     #         user_id = s.loads(token)['user_id']
#     #     except:
#     #         return None
#     #     return User.query.get(user_id)

#     def __repr__(self):
#         return f"User('{self.username}', '{self.email}')"


# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     content = db.Column(db.Text, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

#     def __repr__(self):
#         return f"Post('{self.title}', '{self.date_posted}')"