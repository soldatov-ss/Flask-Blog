import os
import secrets
from PIL import Image
from flaskblog import app
from flask import request, render_template, url_for, flash, redirect
from flaskblog.models import User, Blog
from flaskblog import db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, PostForm, UpdateAccountForm
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



@app.route('/post/new', methods=['POST', 'GET'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Blog(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created', 'success')
        return redirect(url_for('index'))
    return render_template('create_post.html', form=form)


@app.route('/delete-post/<int:id>')
def delete_post(id):
    post = Blog.query.get(id)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect('/my-posts')

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, p_file = os.path.splitext(form_picture.filename)
    picture_new_name = random_hex + p_file
    picture_path = os.path.join(app.root_path, 'static/picture_img', picture_new_name)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_new_name

@app.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename=f'picture_img/{current_user.image_file}')
    return render_template('account.html', form=form, image_file=image_file)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

