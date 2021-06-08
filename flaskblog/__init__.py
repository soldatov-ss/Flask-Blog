from flask import Flask
from  flask_sqlalchemy  import  SQLAlchemy
import os
from flask_ckeditor import CKEditor

app = Flask(__name__)
CKEditor(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(20)
db = SQLAlchemy(app)
db.create_all()