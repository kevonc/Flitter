import sqlite3
from flask import render_template, redirect, url_for, request, g, flash, session
from forms import SignupForm, SigninForm
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
        # user = models.User.get(email=signinform.email.data)
        session['email'] = signinform.email.data
        return redirect(url_for('show_posts'))

@app.route('/logout')
def logout():
    if 'email' not in session:
        return redirect(url_for('index'))
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/flitter')
def show_posts():
    user = { 'nickname': 'Miguel' }
    posts = [
        {
            'author': { 'nickname': 'John' },
            'body': 'Beautiful day in Seattle!'
        },
        {
            'author': { 'nickname': 'Susan' },
            'body': 'Beautiful day in Boston!'
        }
    ]
    return render_template('show_posts.html', title = 'Home', user=user, posts=posts)

@app.route('/flitter/new', methods=['GET', 'POST'])
def new_post():
    return render_template('new_post.html')

@app.route('/user/<username>')
def user_posts(username=None):
    return render_template('show_posts.html', title = 'Home', user=username)