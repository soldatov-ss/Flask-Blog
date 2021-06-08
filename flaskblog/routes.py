from flaskblog import app
from flask import request, render_template, url_for, flash, session, redirect
from flaskblog.models import User, Blog
from werkzeug.security import generate_password_hash, check_password_hash
from flaskblog import db


@app.route('/')
def index():
    all_posts = Blog.query.all()
    if all_posts:
        return render_template('index.html', posts=all_posts)
    return render_template('index.html', posts=None)

@app.route('/register/', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user_info = request.form

        if User.query.filter_by(email=user_info['email']).first():
            flash('Почта уже занята', 'danger')
            return render_template('register.html')
        if User.query.filter_by(username=user_info['username']).first():
            flash('Ник уже занят', 'danger')
            return render_template('register.html')
        if user_info['password'] != user_info['repeatPassword']:
            flash('Passwords do not match! Please try again.', 'danger')
            return render_template('register.html')

        person = User(first_name=user_info['firstname'], last_name=user_info['lastname'], username=user_info['username'],
                      email=user_info['email'], password=generate_password_hash(user_info['password']))
        db.session.add(person)
        db.session.commit()
        flash('Success!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user_info = request.form
        if  User.query.filter_by(username=user_info['username']).first():
            person = User.query.filter_by(username=user_info['username']).first()
            if check_password_hash(person.password, user_info['password']):
                session['login'] = True
                session['first_name'] = person.first_name
                session['last_name'] = person.last_name
                flash(f'Welcome + {session["first_name"]}!', 'success')
            else:
                flash('Password is incorrect!', 'danger')
                return render_template('login.html')
        else:
            flash('User does not exist!', 'danger')
            return render_template('login.html')
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/new-post', methods=['POST', 'GET'])
def create_new_post():
    if request.method == 'POST':
        user_info = request.form
        title = user_info['title']
        author = session['first_name'] + ' ' + session['last_name']
        body = user_info['body_post']
        new_post = Blog(title=title, author=author, body=body)
        db.session.add(new_post)
        db.session.commit()
        flash('Your blogpost is successfully posted!', 'success')
        return redirect('/')
    return render_template('create_new_post.html')


@app.route('/edit-post/<int:id>', methods=['POST', 'GET'])
def edit_post(id):
    print(id)
    if request.method == 'POST':
        new_post = request.form
        old_post = Blog.query.get(id)
        old_post.title = new_post['title']
        # old_post.author = new_post['author']
        old_post.body = new_post['body_post']
        db.session.commit()
        flash('Blog is updated successfully', 'success')
        return redirect(f'/post-id/{id}')
    post = Blog.query.get(id)
    return render_template('edit_post.html', post=post)


@app.route('/post-id/<int:id>')
def one_post(id):
    post = Blog.query.get(id)
    if post:
        return render_template('one_post.html', post=post)
    return render_template('one_post.html', post=None)

@app.route('/my-posts')
def my_all_posts():
    author = session['first_name'] + ' ' + session['last_name']
    all_posts = Blog.query.filter_by(author=author).all()
    if all_posts:
        return render_template('my_all_posts.html', posts=all_posts)
    return render_template('my_all_posts.html', posts=None)


@app.route('/delete-post/<int:id>')
def delete_post(id):
    post = Blog.query.get(id)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect('/my-posts')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out!', 'success')
    return redirect('/')
