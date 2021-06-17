from flask import Flask
from  flask_sqlalchemy  import  SQLAlchemy
from os import urandom, environ
from flask_ckeditor import CKEditor
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
CKEditor(app)
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('DATABASE_URL') or "sqlite:///blog.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = urandom(20)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
# db.create_all()
from flaskblog import routes
