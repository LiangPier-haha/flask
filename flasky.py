from flask import Flask
from flask import request
from flask import make_response
from flask import redirect

app = Flask(__name__)
@app.route('/')
def index():
    return '<h1>Hello World</h1>'
@app.route('/zz')
def zz():
    return '<h2 style="color:red">hello zz</h2>'
@app.route('/zz/<name>')
def helle(name):
    return '<h3>hello %s</h3>' % name
@app.route('/ua')
def ua():
    ua = request.headers.get('User-Agent')
    return '<h1>Your User-Agent is %s</h1>'% ua
@app.route('/cookie')
def cookie():
    response = make_response('<h1>The response carrries a cookie</h1>')
    response.set_cookie('answer','42')
    return response
@app.route('/re')
def redirectTest():
    return redirect('http://www.example.com')
if __name__ == '__main__':
    app.run(debug=True)

