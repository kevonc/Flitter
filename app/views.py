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

    # if user is logged in, skip index page
    if 'username' in session:
        return redirect(url_for('show_posts'))
    else:
        return render_template('index.html', signupform=signupform, signinform=signinform)

@app.route('/signup', methods=['POST'])
def signup():
    signupform = SignupForm()
    signinform = SigninForm()

    if request.method == 'POST':
        input_fullname = signupform.fullname.data
        input_username = signupform.username.data
        input_password = signupform.password.data
        if input_fullname and input_username and input_password:
            # create new user object
            newuser = models.User(fullname=input_fullname, username=input_username, password=input_password)
            db.session.add(newuser)
            db.session.commit()

            # login registered user
            session['username'] = newuser.username
            flash("Thanks for signing up. Now create your first post!")
            return redirect(url_for('index'))
        else:
            return render_template('index.html', signupform=signupform, signinform=signinform)

@app.route('/signin', methods=['POST'])
def signin():
    signupform = SignupForm()
    signinform = SigninForm()

    if request.method == 'POST':
        input_username = signinform.username.data
        input_password = signinform.password.data
        user = models.User.query.filter_by(username=input_username).first()
        if user and user.check_password(input_password):
            session['username'] = input_username
            flash("You've logged in!")
            return redirect(url_for('show_posts'))
        else:
            return render_template('index.html', signupform=signupform, signinform=signinform)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/flitter')
@app.route('/flitter/<int:page>')
def show_posts(page = 1):
    # if user is not logged in, force index page
    if 'username' not in session:
        return redirect(url_for('index'))
    username = session['username']
    user = models.User.query.filter_by(username=username).first()

    # Sorting posts from newest to oldest using timestamp
    posts = user.posts.order_by(models.Post.timestamp.desc()).paginate(page, 10, False)
    return render_template('show_posts.html', title = "%s's Posts" % user.fullname, current_user= None, user=user, posts=posts)

@app.route('/flitter/new', methods=['GET', 'POST'])
def new_post():
    newpostform = NewPost()

    if request.method == 'POST':
        username = session['username']
        user = models.User.query.filter_by(username=username).first()
        content = newpostform.content.data
        now = datetime.datetime.now()
        newpost = models.Post(content=content, timestamp=now, author=user)
        db.session.add(newpost)
        db.session.commit()
        flash("You've added a new post. Good job, keep it up!")
        return redirect(url_for('show_posts'))
    else:
        username = session['username']
        user = models.User.query.filter_by(username=username).first()
        return render_template('new_post.html', newpostform=newpostform, user=user)

@app.route('/flitter/<username>')
@app.route('/flitter/<username>/<int:page>')
def user_posts(username = None, page = 1):
    user = models.User.query.filter_by(username=username).first()
    posts = user.posts.order_by(models.Post.timestamp.desc()).paginate(page, 10, False)

    if 'username' not in session:
        current_user = None
    else:
        current_username = session['username']
        current_user = models.User.query.filter_by(username=current_username).first()

    return render_template('show_posts.html', title = "%s's Posts" % user.fullname, current_user=current_user, user=user, posts=posts)