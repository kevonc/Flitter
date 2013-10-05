import sqlite3
import datetime
from flask import render_template, redirect, url_for, request, g, flash, session
from forms import SignupForm, SigninForm, NewPost
from app import app, db, models
from models import db, User

app.secret_key = 'development key'

@app.route('/')
def index():
    signupform = SignupForm()
    signinform = SigninForm()

    if 'email' in session:
        return redirect(url_for('show_posts'))
    else:
        return render_template('index.html', signupform=signupform, signinform=signinform)

@app.route('/signup', methods=['POST'])
def signup():
    signupform = SignupForm()
    signinform = SigninForm()

    if request.method == 'POST':
        print 'work'
        newuser = models.User(fullname=signupform.fullname.data, email=signupform.email.data, password=signupform.password.data)
        db.session.add(newuser)
        db.session.commit()

        session['email'] = newuser.email
        return redirect(url_for('index'))

@app.route('/signin', methods=['POST'])
def signin():
    signupform = SignupForm()
    signinform = SigninForm()

    if request.method == 'POST':
        input_email = signinform.email.data
        input_password = signinform.password.data
        user = models.User.query.filter_by(email=input_email).first()
        if user and user.password == input_password:
            print user.email
            session['email'] = input_email
            return redirect(url_for('show_posts'))
        else:
            return render_template('index.html', signupform=signupform, signinform=signinform)

@app.route('/logout')
def logout():
    if 'email' not in session:
        return redirect(url_for('index'))
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/flitter')
def show_posts():
    email = session['email']
    user = models.User.query.filter_by(email=email).first()
    posts = user.posts.all()
    return render_template('show_posts.html', title = "%s's Posts" % user.fullname, user=user, posts=posts)

@app.route('/flitter/new', methods=['GET', 'POST'])
def new_post():
    newpostform = NewPost()

    if request.method == 'POST':
        email = session['email']
        user = models.User.query.filter_by(email=email).first()
        content = newpostform.content.data
        now = datetime.datetime.now()
        newpost = models.Post(content=content, timestamp=now, author=user)
        db.session.add(newpost)
        db.session.commit()
        return redirect(url_for('show_posts'))
    else:
        email = session['email']
        user = models.User.query.filter_by(email=email).first()
        return render_template('new_post.html', newpostform=newpostform, user=user)

@app.route('/user/<username>')
def user_posts(username=None):
    # will have to change to username later
    user = models.User.query.filter_by(fullname=username).first()
    posts = user.posts.all()
    return render_template('show_posts.html', title = 'Home', user=user, posts=posts)