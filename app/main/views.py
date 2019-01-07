from .forms import NameForm
from flask import redirect,session,url_for,render_template,current_app
from app.models import User
from app.email import send_mail
from app import create_app,db
from . import main
import os

@main.route('/',methods=['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if user is None:
            user = User(name=form.name.data)
            db.session.add(user)
            session['known'] = False
            if current_app.config['FLASKY_ADMIN']:
                send_mail(current_app.config['FLASKY_ADMIN'],'New User','mail/new_user',user=user)
        else:
            session['known'] = True

        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('index.html',name=session.get('name'),form=form,known = session.get('known',False))
