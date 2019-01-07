from flask import current_app,render_template
from . import mail
from flask_mail import Message
from threading import Thread


def send_async_mail(app,msg):
    with app.app_context():

        mail.send(msg)
        print(1)

def send_mail(to,subject,template,**keyword):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+''+subject,sender=app.config['FLASKY_MAIL_SENDER'],recipients=[to])
    msg.body = render_template(template+'.txt',**keyword)
    msg.html = render_template(template+'.html',**keyword)
    thread = Thread(target = send_async_mail,args=[app,msg])
    thread.start()
    return thread
#    with app.app_context():
#        mail.send(msg)
#        print(1)
