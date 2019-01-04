import os
from flask_bootstrap import Bootstrap
from datetime import datetime
from flask import Flask, render_template,url_for,flash,session,redirect
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,validators
from flask_moment import Moment
from flask_script import Manager,Shell
from flask_sqlalchemy import SQLAlchemy


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
#定义模型
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


class NameForm(FlaskForm):
    name = StringField('你叫什么名字',validators=[validators.Required()])
    submit = SubmitField('提交')


@app.route('/',methods=["GET","POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        user = User.query.filter_by(name=name).first()
        if user:
            session['known'] = True
        else:
            user = User(name=name)
            db.session.add(user)
            db.session.commit()

            session['known'] = False
        session['name'] = name
        return redirect(url_for('index'))
    print(session.get('known'))
    return render_template('index1.html',form = form,known=session.get('known',False) ,name = session.get('name'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'),500

def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role)
if __name__ == '__main__':
    db.create_all()
    manager.add_command('shell',Shell(make_context=make_shell_context))
    manager.run()
