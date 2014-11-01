from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from flask import current_app
from .permission import Permission
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