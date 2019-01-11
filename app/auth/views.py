from . import auth
from .forms import LoginForm,RegisteForm,ResetPasswordForm,SetPasswordForm,ChangePasswordForm,ChangeEmailForm
from flask import render_template,url_for,redirect,flash,request
from ..models import User
from ..email import send_mail
from .. import db
from flask_login import login_user,logout_user,current_user,login_required

@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        password =form.password.data
 #       print(email,password,user.name)
        if user is not None and user.verify_password(password):
            login_user(user,form.remeber_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password')
    return render_template('auth/login.html',form=form)


@auth.route('/logout')
def logout():
    logout_user()
    flash('You have logged out!')
    return redirect(url_for('main.index'))


@auth.route('/registe',methods=['GET','POST'])
def register():
    form = RegisteForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,name=form.username.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generat_confirmation_token()
        send_mail(form.email.data,'Confirm Your Account','auth/email/confirm',user=user,token=token)
        flash('A confirmed email has been sent to you by email.')
        return redirect(url_for('main.index'))
    return render_template('auth/registe.html',form = form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirm your account. Thanks!')
    else:
        flash('The confirm link is invalid or has expired.')
    return redirect(url_for('main.index'))
@auth.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.confirmed \
            and request.endpoint and request.endpoint[:5]!='auth.' \
            and request.endpoint !='static':
        print(1)
        return redirect(url_for('auth.unconfirmed'))
@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        print(2)
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/resend_confirmation')
@login_required
def resend_confirmation():
    token = current_user.generat_confirmation_token()
    send_mail(current_user.email,'Confirm your account,Thanks!','auth/email/confirm',user=current_user,token=token)
    flash('A confirmation has sent your email!')
    return redirect(url_for('auth.unconfirmed'))

@auth.route('/reset_password',methods=['GET','POST'])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            send_mail(user.email,'Reset your password of your account','auth/email/reset_password',user=user,token=user.generate_reset_token())
            flash('A reset password email has been sent to your email!')
        else:
            flash('The email is invalid,check and rewrite')
    return render_template('auth/reset_password.html',form=form)

@auth.route('/set_password/<token>',methods=['GET','POST'])
def set_password(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = SetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            if user.reset_password(token,form.password.data):
                flash('Your password has reseted!')
                return redirect(url_for('auth.login'))
            else:
                flash('修改失败')
                return redirect(url_for('main.index'))
        else:
            flash('The email is invalid')
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html',form=form)

@auth.route('/chang_password',methods=['GET','POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            logout_user()
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
    return render_template('auth/change_password.html',form=form)

@auth.route('/change_email',methods=['GET','POST'])
@login_required
def change_email():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            token = current_user.generate_changeemail_token(form.email.data)
            send_mail(form.email.data,'Change your email','auth/email/change_email',user=current_user,token=token)
            flash('A email has been sent to the new email')
            return redirect(url_for('main.index'))
    return render_template('auth/change_email.html',form=form)

@auth.route('/set_email/<token>',methods=['GET','POST'])
def set_email(token):
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            if current_user.change_email(token,form.email.data):
                flash('Your email has been updated,please relogin.')
                return redirect(url_for('auth.login'))
            flash('The email is invalid.')
            return redirect(url_for('auth.set_email',token=token))
        flash('The password is false.')
        return redirect(url_for('auth.set_email',token=token))
    return render_template('auth/change_email.html',form=form)

