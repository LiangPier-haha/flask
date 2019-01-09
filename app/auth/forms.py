from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms import ValidationError
from ..models import User
from wtforms.validators import Required,Length,Email,Regexp,EqualTo



class LoginForm(FlaskForm):
    email = StringField('邮箱',validators = [Required(),Length(1,64),Email()])
    password = PasswordField('密码',validators = [Required()])
    remeber_me = BooleanField('记住我')
    submit = SubmitField('登陆')


class RegisteForm(FlaskForm):
    email = StringField('Email',validators=[Required(),Length(1,64),Email()])
    username = StringField('Username',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must have only letters,number,dots or underscores')])
    password = PasswordField('Password',validators=[Required(),EqualTo('password2',message='Password must be match.')])
    password2 = PasswordField('Confirm password',validators = [Required()])
    submit = SubmitField('Register')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

    def validate_username(self,field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('Username already in use.')

class ResetPasswordForm(FlaskForm):
    email = StringField('Email',validators=[Required(),Length(1,64),Email()])
    submit = SubmitField('发送邮件')


class SetPasswordForm(FlaskForm):
    email = StringField('Email',validators=[Required(),Length(1,64),Email()])
    password = PasswordField('New Password',validators=[Required(),EqualTo('password2',message='Password must match')])
    password2 = PasswordField('Confirm Password',validators=[Required()])
    submit = SubmitField('重置密码')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Uknown email address')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password',validators=[Required()])
    password = PasswordField('Password',validators=[Required(),EqualTo('password2',message='Password must metch')])
    password2 = PasswordField('Confirm Password',validators=[Required()])
    submit = SubmitField('提交')


class ChangeEmailForm(FlaskForm):
    email = StringField('New Email',validators=[Required(),Length(1,64),Email()])
    password = PasswordField('Password',validators=[Required()])
    submit = SubmitField('提交')
