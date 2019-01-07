from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,validators

class NameForm(FlaskForm):
    name = StringField('你的名字是什么',validators=[validators.Required()])
    submit = SubmitField('提交')
