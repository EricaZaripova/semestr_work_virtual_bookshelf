import os

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from virtual_bookshelf import db
from auth.databases import get_profile_by_id
from user.forms import ProfileForm


user = Blueprint('user', __name__, template_folder='templates', static_folder='static')
upload_files_dir = 'avatar'


@user.route('/', methods=['GET'])
@login_required
def user_page():
    return render_template('user_page.html', user=current_user, profile=get_profile_by_id(current_user.id))


@user.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    user = current_user
    profile = get_profile_by_id(current_user.id)

    if form.validate_on_submit():
        avatar = form.avatar.data
        if avatar:
            download_avatar(avatar, profile)
        if check_password_hash(user.password, form.old_password.data):
            user.email = form.email.data
            user.username = form.username.data
            if form.new_password.data:
                if len(form.new_password.data) >= 8:
                    user.password = generate_password_hash(form.new_password.data)
                else:
                    flash('Новый пароль должен содержать не менее 8 символов', category='danger')
            profile.birthdate = form.birthdate.data
            db.session.add(user, profile)
            db.session.commit()
            flash('Изменения сохранены', category='success')
            return redirect(url_for('user.user_page', user=user, profile=profile))
        else:
            flash('Неверный пароль', category='danger')
    else:
        form.email.data = user.email
        form.username.data = user.username
        form.old_password.data = None
        form.new_password.data = None
        form.birthdate.data = profile.birthdate

    return render_template('profile.html', form=form)


def download_avatar(avatar, profile):
    if profile.avatar:
        os.remove(os.path.join('static', upload_files_dir, profile.avatar))
    name, ext = avatar.filename.rsplit('.', 1)
    avatar_name = generate_password_hash(name)[-30:] + '.' + ext
    avatar_path = os.path.join(upload_files_dir, avatar_name)
    avatar.save(os.path.join('static', avatar_path))
    profile.avatar = avatar_path
