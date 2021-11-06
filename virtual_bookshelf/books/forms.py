import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TextAreaField
from wtforms.validators import DataRequired


class BooksBaseForm(FlaskForm):
    name = StringField("Название книги: ", validators=[DataRequired('Заполните поле')])
    author = StringField("Автор: ", validators=[DataRequired('Заполните поле')])
    link = StringField("Ссылка на электронный источник: ", default='-')


class BooksAlreadyReadForm(BooksBaseForm):
    columns = ["Название", 'Автор', "Ссылка", "Начало чтения", "Конец чтения", "Мнение"]
    beginning_at = DateField('Начало чтения (формат даты дд/мм/гггг):', default=datetime.date.today(),
                             format='%d/%m/%Y', validators=[DataRequired('Заполните поле')])
    ending_at = DateField('Конец чтения (формат даты дд/мм/гггг):', default=datetime.date.today(),
                          format='%d/%m/%Y', validators=[DataRequired('Заполните поле')])
    opinion_about = TextAreaField('Мнение о книге: ', default='-')

    submit = SubmitField('Сохранить книгу')


class BooksInTheProcessForm(BooksBaseForm):
    columns = ["Название", 'Автор', "Ссылка", "Начало чтения"]
    beginning_at = DateField('Начало чтения (формат даты дд/мм/гггг):',
                             format='%d/%m/%Y',
                             validators=[DataRequired('Заполните поле')])

    submit = SubmitField('Сохранить книгу')


class BooksForTheFutureForm(BooksBaseForm):
    columns = ["Название", 'Автор', "Ссылка"]
    submit = SubmitField('Сохранить книгу')


class QuotesForm(FlaskForm):
    text = TextAreaField("Цитата", validators=[DataRequired('Заполните поле')])
    speaker = StringField("Автор цитаты: ", default='-', validators=[])
    place = StringField("Место (глава/часть и т.д.)", default='-')

    submit = SubmitField('Добавить цитату')
