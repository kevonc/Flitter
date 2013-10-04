from flask import render_template, redirect
from app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return redirect(url_for('show_posts'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return redirect(url_for('show_posts'))

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