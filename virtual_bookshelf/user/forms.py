from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import Email, Length, DataRequired


class ProfileForm(FlaskForm):
    email = StringField('Email: ',
                        validators=[Email("Некоректный Email"), Length(max=30), DataRequired('Заполните поле')])
    username = StringField('Имя пользователя: ',
                           validators=[Length(min=4, max=30,
                                              message="Имя пользователя должно содержать от 4 до 30 символов"),
                                       DataRequired('Заполните поле')])
    old_password = PasswordField('Старый пароль: ', validators=[Length(min=8, max=30,
                                                                message="Пароль должен содержать от 8 до 30 символов"),
                                                         DataRequired('Заполните поле')])
    new_password = PasswordField('Новый пароль: ', validators=[Length(max=30, message="Пароль должен содержать от 8 до 30 символов")])
    avatar = FileField("Аватар", validators=[FileAllowed(['jpg','jpeg','png'], message='Недопустимый формат изображения')])
    birthdate = DateField('Дата рождения (формат даты дд/мм/гггг)', default=None, format='%d/%m/%Y', validators=[DataRequired('Заполните поле')])

    submit = SubmitField('Сохранить')
