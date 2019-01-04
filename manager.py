from flask import Flask
from flask import request
from flask import make_response
from flask import redirect
from flask_script import Manager

app = Flask(__name__)
manager = Manager(app)
@app.route('/')
def index():
    return '<h1>Hello World</h1>'
@app.route('/zz')
def zz():
    return '<h2 style="color:red">hello zz</h2>'
@app.route('/zz/<name>')
def helle(name):
    return '<h3>hello %s</h3>' % name/0
@app.route('/ua')
def ua():
    ua = request.headers.get('User-Agent')
    return '<h1>Your User-Agent is %s</h1>'% ua
@app.route('/cookie')
def cookie():
    response = make_response('<h1>The response carrries a cookie</h1>')
    response.set_cookie('answer','42')
    return response
@app.before_first_request
def gouzi_first_request():
    print('before first request')
@app.before_request
def gouzi_before_request():
    print('before request')
    print('request-path',request.path)
    print('request-method',request.method)
    print('request-headers',request.headers)
@app.teardown_request
def gouzi_teardown_request(e):
    print('teardown request',e)
@app.route('/re')
def redirectTest():
    return redirect('http://www.example.com')
@app.after_request
def gouzi(response):
    print('hah')
    return response
@app.route('/400')
def status_400():
    return '<h3>返回400状态码</h3>',400
if __name__ == '__main__':
    manager.run()

