from . import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash,check_password_hash
from . import login_manager
from flask_login import UserMixin,current_user
from flask import current_app


class Role(db.Model):
    __tablename__='roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,unique=True)
    default = db.Column(db.Boolean,default=False,index=True)
    users = db.relationship('User',backref='role',lazy='dynamic')
    permisson = db.Column(db.Integer)

    def __repr__(self):
        return '<Role %r>'% self.name


class Permission():
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICAL = 0x04
    MODIFI_COMMENT = 0x08
    ADMIN = 0xff


class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String,unique=True,index=True)
    name = db.Column(db.String,unique=True,index=True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean,default=False)
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)

    def verify_password(self,password):
        print(check_password_hash(self.password_hash,password))
        return check_password_hash(self.password_hash,password)

    def generat_confirmation_token(self,expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'confirm':self.id})
    def confirm(self,token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self,expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'reset':self.id})
    def reset_password(self,token,password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = password
        db.session.add(self)
        return True

    def generate_changeemail_token(self,expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'change_email':self.id})
    def change_email(self,token,email):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        self.email = email
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>'% self.name

@login_manager.user_loader
def load_user(user_id):
    print('回调执行')
    return User.query.get(int(user_id))
