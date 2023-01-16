from flask import Flask, render_template, redirect, \
    url_for,request, make_response, abort, session, flash
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/hello/<user>')
def hello(user):
    return render_template('hello.html', name=user)
    
@app.route('/success/<name>')
def success(name):
    return 'welcome %s' %name

@app.route('/grade', methods=['POST','GET'])
def grade():
    if request.method=='POST':
        results = request.form
        return render_template('results.html',results=results, username=request.cookies.get('username'))
    return render_template('grades.html', username=request.cookies.get('username'))
    


@app.route('/results', methods=['GET','POST'])
def results():
    results = {}
    if request.method=='GET':
        for key,value in request.args.items():
            results[key]=value
    elif request.method=='POST':
        results = request.form
    if len(results)==0:
        results = {'math':85,'english':90,'hisory': 75}
    return render_template('results.html',results=results, username=request.cookies.get('username'))

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method=='POST':
        user = request.form['nm']
        password = request.form['password']
        if user not in users.keys() or password != users[user]:
            flash('No such user')
            flash('please sign up')
            return redirect(url_for('index'))

        resp = make_response(redirect(url_for('grade')))
        resp.set_cookie('username', user)
        session['user']=user
        if user=='rick':
            abort(401)
        return resp
    else:
        user = request.args.get('nm')
        return redirect(url_for('grade'))

users = {'admin':'admin','danny':'danny','roza':'roza'}
app.secret_key="secret_key"

if __name__ == '__main__':
    app.run(debug=True)