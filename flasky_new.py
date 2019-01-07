from flask import Flask,render_template,session,flash,redirect,url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_script import Manager,Shell
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField,SubmitField,validators
from datetime import datetime
from flask_migrate import Migrate,MigrateCommand
from flask_mail import Mail,Message
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data1.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[FLASKY]'
app.config['FLASKY_MAIL_SENDER'] = 'Flask Admin <flasky@example.com>'
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')
manager = Manager(app)
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
migrate = Migrate(app,db)
mail = Mail(app)


#class Role(db.Model):
#    __tablename__= 'roles'
#    id = db.Column(db.Integer,primary_key=True)
#    name = db.Column(db.String(64),unique=True)
#    users = db.relationship('User',backref='role',lazy='dynamic')
#
#    def __repr__(self):
#        return '<Role %r>'% self.name
class Role(db.Model):
     __tablename__ = 'roles'
     id = db.Column(db.Integer,primary_key=True)
     name = db.Column(db.String(64),unique=True)
     users = db.relationship('User',backref='role',lazy='dynamic')
     def __repr__(self):
         return '<Role %r>'% self.name

class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>'% self.name


def make_shell_context():
    return dict(db=db,app=app,User=User,Role=Role)
manager.add_command('shell',Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)
class NameForm(FlaskForm):
    name = StringField('你的名字是什么',validators=[validators.Required()])
    submit = SubmitField('提交')
def send_mail(to,subject,template,**keyword):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+''+subject,sender=app.config['FLASKY_ADMIN'],recipients=[to])
    msg.body = render_template(template+'.txt',**keyword)
    msg.html = render_template(template+'.html',**keyword)
    mail.send(msg)
@app.route('/',methods=['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name = form.name.data).first()
        if user:
            #flash('你似乎更改了你的名字')
            print(user)

            session['known'] = True
        else:
            user = User(name = form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            send_mail(app.config['FLASKY_ADMIN'],'New User','mail/new_user',user=user)
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html',known = session.get('known',False),name = session.get('name'),form = form)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

if __name__=='__main__':
    manager.run()






