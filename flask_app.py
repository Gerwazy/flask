from flask import Flask, render_template, url_for, flash, redirect, json, session, Response, request
from forms import LoginForm
from datetime import timedelta
import time

app = Flask(__name__)

app.config['SECRET_KEY'] = '9a1b5091aa7f9a2201b315c2d241c78f'
app.permanent_session_lifetime = timedelta(hours = 2)

def get_users():
    users = json.load(open('static/data/users.json'))
    return users

def del_users(name):
    users = json.load(open('static/data/users.json'))
    try:
        if name != session["user"]:
            del users[name]
            open('static/data/users.json', "w").write(
            json.dumps(users, sort_keys=True)
            )
    except:
        pass

def add_users(username, password):
    users = json.load(open('static/data/users.json'))
    users[username] = password
    open('static/data/users.json', "w").write(
        json.dumps(users, sort_keys=True)
    )

def get_message():
    time.sleep(1)
    s = time.ctime(time.time())
    return s


@app.route('/')
def home():
    return render_template('public/home.html')


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if "user" in session:
        return render_template('admin/admin.html')
    else:
        form = LoginForm()
        if form.validate_on_submit():
            users = get_users()
            if form.username.data in users and users[form.username.data] == form.password.data:
                session["user"] = form.username.data
                flash('Zalogowano pomyślnie!', 'success')
                return redirect(url_for('admin'))
            else:
                flash('Nieprawidłowy login lub hasło!', 'danger')
        return render_template('public/login.html', form=form)


@app.route('/admin', methods = ['POST', 'GET'])
def admin():
    if "user" in session:
        if request.method == 'POST':
            user = request.form['username']
            password = request.form['password']
            add_users(user,password)
        users = get_users()
        return render_template('admin/admin.html', data=users)
    else:
        return redirect(url_for('login'))

@app.route('/delete/<name>')
def delete(name):
    if "user" in session:
        del_users(name)
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('login'))

@app.route('/sse')
def sse():
    if "user" in session:
        return render_template('admin/sse.html')
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('home'))


@app.route('/stream')
def stream():
    def eventStream():
        while True:
            yield 'data: {}\n\n'.format(get_message())
    return Response(eventStream(), mimetype="text/event-stream")

if __name__ == '__main__':
    app.run(debug=True)

