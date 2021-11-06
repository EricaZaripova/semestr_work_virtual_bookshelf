from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate


from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
SECRET_KEY = 'gheghgj3qhgt4q$#^#$hedjsb'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Kshish27@localhost:5432/bookshelf"
app.config.from_object(__name__)

db = SQLAlchemy()
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = 'warning'

migrate = Migrate(app, db)

bootstrap = Bootstrap(app)


from virtual_bookshelf.auth.auth import auth
app.register_blueprint(auth)

from virtual_bookshelf.user.user import user
app.register_blueprint(user, url_prefix='/user')

from virtual_bookshelf.books.books import books
app.register_blueprint(books)
