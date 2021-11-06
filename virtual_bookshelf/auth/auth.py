from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from virtual_bookshelf import db
from auth.forms import RegistrationForm, LoginForm
from auth.databases import get_profile_by_id, get_user
from auth.models import Profile, User


auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static')


@auth.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.user_page', user=current_user, profile=get_profile_by_id(current_user.id)))

    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = get_user(form.email.data)
            if user and check_password_hash(user.password, form.password.data):
                print(form.remember.data)
                login_user(user, remember=form.remember.data)
                return redirect(url_for('user.user_page', user=current_user, profile=get_profile_by_id(current_user.id)))
            else:
                flash('Неверные email или пароль', category='Danger')
    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта', category='success')
    return redirect(url_for('main'))


@auth.route('/registration', methods=['POST', 'GET'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('user.user_page', user=current_user, profile=get_profile_by_id(current_user.id)))

    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if not get_user(form.email.data):
                password = generate_password_hash(form.password.data)
                new_user = User(email=form.email.data, username=form.username.data, password=password)
                try:
                    db.session.add(new_user)
                    db.session.commit()
                    login_user(new_user)
                    profile = Profile(user_id=current_user.id)
                    db.session.add(profile)
                    db.session.commit()
                    return redirect(url_for('user.user_page'))
                except Exception as e:
                    flash(f'Ошибка добавления: {e}', category='danger')
                return redirect(url_for('user.user_page', user=current_user, profile=get_profile_by_id(current_user.id)))
            else:
                flash('Email уже зарегистрирован', category='danger')
    return render_template('registration.html', form=form)

