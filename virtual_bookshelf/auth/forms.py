from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Email, Length, EqualTo, DataRequired


class LoginForm(FlaskForm):
    email = StringField('Email: ', validators=[Email("Некоректный Email"), DataRequired('Заполните поле')])
    password = PasswordField('Пароль: ', validators=[Length(min=8, max=30,
                                                            message="Пароль должен содержать от 8 до 30 символов"),
                                                     DataRequired('Заполните поле')])
    remember = BooleanField("Запомнить", default=False)
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    email = StringField('Email: ', validators=[Email("Некоректный Email"), Length(max=30), DataRequired('Заполните поле')])
    username = StringField('Имя пользователя: ',
                           validators=[Length(min=4, max=30,
                                              message="Имя пользователя должно содержать от 4 до 30 символов"),
                                       DataRequired('Заполните поле')])
    password = PasswordField('Пароль: ', validators=[Length(min=8, max=30,
                                                            message="Пароль должен содержать от 8 до 30 символов"),
                                                     DataRequired('Заполните поле')])
    password2 = PasswordField('Повторите пароль: ',
                              validators=[EqualTo('password', message="Пароли не совпадают")])
    submit = SubmitField('Зарегистрироваться')