from flask_login import UserMixin

from virtual_bookshelf import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(30), unique=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'{self.email}, {self.username}, {self.password}'


class Profile(db.Model):
    __tablename__ = 'users_profile'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    avatar = db.Column(db.String())
    birthdate = db.Column(db.Date)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

    def __repr__(self):
        return f"{self.id}, ({self.user_id})"
