from virtual_bookshelf import db
from auth.models import User, Profile


def get_user(email):
    return db.session.query(User).filter(User.email == f"{email}").first()


def get_profile_by_id(user_id):
    return db.session.query(Profile).filter(Profile.user_id == user_id).first()