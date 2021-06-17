from flaskblog import app
from flask import request, render_template, url_for, flash, session, redirect
from flaskblog.models import User, Blog
from flaskblog import db, login_manager, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flask_login import current_user, login_user, logout_user, login_required


@app.route('/')
def index():
    # all_posts = Blog.query.all()
    # if all_posts:
    #     return render_template('index.html', posts=all_posts)
    return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)



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
    if request.method == 'POST':
        new_post = request.form
        old_post = Blog.query.get(id)
        old_post.title = new_post['title']
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
    logout_user()
    return redirect(url_for('index'))

