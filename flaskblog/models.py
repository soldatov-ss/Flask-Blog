from flaskblog import db

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), index=True)
    last_name = db.Column(db.String(20), index=True)
    username = db.Column(db.String(30), unique=True, index=True)
    email = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(200))

class Blog(db.Model):
    blog_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(40))
    body = db.Column(db.String(1000))

