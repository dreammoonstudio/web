from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'Newbie': (Permission.FOLLOW, True),
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.CREATE_POST, False),
            'Advanced User': (0x00f | Permission.CREATE_PAGE |
                              Permission.CREATE_TOPIC, False),
            'Moderator': (0x0ff, False),
            'Administer': (0xfff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = role[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirm = True
        db.session.add(self)
        return True

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['DM_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xfff).first()
            else:
                self.role = Role.query.filter_by(default=True).first()

@login_manager.user_loader
def login_user(user_id):
    return User.query.get(int(user_id))