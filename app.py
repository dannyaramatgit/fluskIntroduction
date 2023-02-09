
from flask import Flask, render_template, redirect, \
    url_for, request, make_response, abort, session, flash, g
from markupsafe import escape
import logging
from logging.handlers import SysLogHandler
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
CSRFProtect(app)


@app.before_request
def fix_missing_csrf_token():
    if app.config['WTF_CSRF_FIELD_NAME'] not in session:
        if app.config['WTF_CSRF_FIELD_NAME'] in g:
            g.pop(app.config['WTF_CSRF_FIELD_NAME'])


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/hello/<user>')
def hello(user):
    return render_template('hello.html', name=user)


@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name


@app.route('/grade', methods=['POST', 'GET'])
def grade():
    if request.method == 'POST':
        results = request.form
        return render_template('results.html', results=results, username=request.cookies.get('username'))
    return render_template('grades.html', username=request.cookies.get('username'))


@app.route('/results', methods=['GET', 'POST'])
def results():
    results = {}
    if request.method == 'GET':
        for key, value in request.args.items():
            results[key] = value
    elif request.method == 'POST':
        results = request.form
    if len(results) == 0:
        results = {'math': 85, 'english': 90, 'hisory': 75}
    return render_template('results.html', results=results, username=request.cookies.get('username'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        password = request.form['password']
        if user not in users.keys() or password != users[user]:
            flash('No such user')
            flash('please sign up')
            return redirect(url_for('index'))

        resp = make_response(redirect(url_for('grade')))
        resp.set_cookie('username', user)
        session['user'] = user
        if user == 'rick':
            abort(401)
        return resp
    else:
        user = request.args.get('nm')
        return redirect(url_for('grade'))


users = {'admin': 'admin', 'danny': 'danny', 'roza': 'roza'}
app.secret_key = "secret_key"

# Create a custom logger
logger = logging.getLogger(__name__)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('file.log')
c_handler.setLevel(logging.WARNING)
f_handler.setLevel(logging.ERROR)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)


if __name__ == '__main__':

    logger.warning('This is a warning')
    logger.error('This is an error')
    app.run(host="0.0.0.0", debug=True)
