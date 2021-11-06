from flask import render_template, flash, redirect, url_for, Blueprint, json, request
from flask_login import login_required, current_user

from books.databases import get_already_read_books, get_in_the_process_books, \
    get_for_the_future_books, get_book_by_id, get_quotes_by_book_id, get_quote_by_id, get_all_book
from books.forms import BooksAlreadyReadForm, BooksInTheProcessForm, \
    BooksForTheFutureForm, QuotesForm
from books.models import db, AlreadyRead, InTheProcess, ForTheFuture, Quotes


books = Blueprint('books',  __name__, template_folder='templates', static_folder='static')


@books.route('/add_book/<string:type_of_list>', methods=['GET', 'POST'])
@login_required
def add_book(type_of_list):
    if type_of_list == 'already_read':
        form = BooksAlreadyReadForm()
    elif type_of_list == 'in_the_process':
        form = BooksInTheProcessForm()
    elif type_of_list == 'for_the_future':
        form = BooksForTheFutureForm()

    if form and form.validate_on_submit():
        if form.name.data not in check_the_books_name(current_user.id):
            new_book = fill_book(type_of_list, form)
            try:
                db.session.add(new_book)
                db.session.commit()
                flash('Книга добавлена', category='success')
            except Exception as e:
                flash(f'Ошибка добавления: {e}', category='danger')
        else:
            flash('Книга с таким названием уже существует', category='danger')
    return render_template('add_book.html', form=form, type_of_list=type_of_list)


@books.route('/move_book/<string:type_of_list_old>/<string:type_of_list_new>/<int:book_id>', methods=['GET', 'POST'])
@login_required
def move_book(type_of_list_old, type_of_list_new, book_id):
    book = get_book_by_id(type_of_list_old, book_id)
    if type_of_list_new == 'already_read':
        form = BooksAlreadyReadForm()
    elif type_of_list_new == 'in_the_process':
        form = BooksInTheProcessForm()
    elif type_of_list_new == 'for_the_future':
        form = BooksForTheFutureForm()

    form.name.data = book.name
    form.author.data = book.author
    form.link.data = book.link

    if form and form.validate_on_submit():
        new_book = fill_book(type_of_list_new, form)
        try:
            db.session.add(new_book)
            db.session.delete(book)
            db.session.commit()
            flash('Книга перемещена', category='success')
            return redirect(url_for('.book_page', type_of_list=type_of_list_new, book_id=new_book.id))
        except Exception as e:
            flash(f'Ошибка добавления: {e}', category='danger')

    return render_template('move_book.html', type_of_list_old=type_of_list_old, type_of_list_new=type_of_list_new, book_id=book.id, book=book, form=form)


@books.route('/book_page/<string:type_of_list>/<int:book_id>', methods=['GET'])
@login_required
def book_page(type_of_list, book_id):
    book = get_book_by_id(type_of_list, book_id)
    if book:
        if type_of_list == 'already_read':
            quotes = get_quotes_by_book_id(book_id)
            return render_template('book_page_already_read.html', type_of_list=type_of_list, book=book, quotes=quotes)
        return render_template(f'book_page_{type_of_list}.html', type_of_list=type_of_list, book=book)
    return render_template('404.html'), 404


@books.route('/list_of_book/<string:type_of_list>', methods=['GET'])
@login_required
def list_of_book(type_of_list):
    if type_of_list == 'already_read':
        books = get_already_read_books(current_user.id)
        columns = BooksAlreadyReadForm().columns
    elif type_of_list == 'in_the_process':
        books = get_in_the_process_books(current_user.id)
        columns = BooksInTheProcessForm().columns
    elif type_of_list == 'for_the_future':
        books = get_for_the_future_books(current_user.id)
        columns = BooksForTheFutureForm().columns
    else:
        books = None
        columns = None

    return render_template('list_of_books.html', type_of_list=type_of_list, books=books, columns=columns)


@books.route('/edit_a_book/<string:type_of_list>/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_a_book(type_of_list, book_id):
    book = get_book_by_id(type_of_list, book_id)
    form = fill_form(type_of_list, book)

    if form.validate_on_submit():
        book.name = form.name.data
        book.author = form.author.data
        book.link = form.link.data
        if type_of_list in ['already_read', 'in_the_process']:
            book.beginning_at = form.beginning_at.data
            if type_of_list == 'already_read':
                book.ending_at = form.ending_at.data
                book.opinion_about = form.opinion_about.data

        try:
            db.session.add(book)
            db.session.commit()
            flash('Изменения сохранены', category='success')
        except Exception as e:
            flash(f'Ошибка добавления: {e}', category='danger')

    return render_template('edit_a_book.html', type_of_list=type_of_list, book_id=book.id, book=book, form=form)


@books.route('/add_quote/<string:type_of_list>/<int:book_id>', methods=['GET', 'POST'])
@login_required
def add_quote(type_of_list, book_id):
    book = get_book_by_id(type_of_list, book_id)
    form = QuotesForm()
    quotes = get_quotes_by_book_id(book_id)
    if form.validate_on_submit():
        quote = Quotes(text=form.text.data,
                       speaker=form.speaker.data,
                       place=form.place.data,
                       book_id=book_id)
        try:
            db.session.add(quote)
            db.session.commit()
            flash('Цитата добавлена', category='success')
            return redirect(url_for('.book_page', type_of_list=type_of_list, book_id=book_id, quotes=quotes))
        except Exception as e:
            flash(f'Ошибка добавления: {e}', category='danger')

    return render_template('add_quote.html', type_of_list=type_of_list, book_id=book_id, form=form, book=book)


@books.route('/delete_book/<string:type_of_list>/<int:book_id>')
@login_required
def delete_book(type_of_list, book_id):
    book = get_book_by_id(type_of_list, book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('.list_of_book', type_of_list=type_of_list))


@books.route('/delete_quote/already_read/<int:book_id>/<int:quote_id>')
@login_required
def delete_quote(book_id, quote_id):
    quotes = get_quotes_by_book_id(book_id)
    quote = get_quote_by_id(quote_id)
    db.session.delete(quote)
    db.session.commit()
    return redirect(url_for('.book_page', type_of_list='already_read', book_id=book_id, quotes=quotes))


@books.route('/ajax', methods=['GET', 'POST'])
@login_required
def ajax():
    type_of_list = str(request.form.get('type_of_list'))
    book_id = int(request.form.get('book_id'))
    book = get_book_by_id(type_of_list, book_id)
    return 'Прочитано за '+str((book.ending_at-book.beginning_at).days) + ' суток'


def check_the_books_name(user_id):
    books_name = []
    res = get_all_book(user_id)
    for book in res:
        books_name.append(book[0])
    return books_name


def fill_form(type_of_list, book):
    if type_of_list == 'already_read':
        form = BooksAlreadyReadForm(name=book.name,
                                    author=book.author,
                                    link=book.link,
                                    beginning_at=book.beginning_at,
                                    ending_at=book.ending_at,
                                    opinion_about=book.opinion_about)
    elif type_of_list == 'in_the_process':
        form = BooksInTheProcessForm(name=book.name,
                                     author=book.author,
                                     link=book.link,
                                     beginning_at=book.beginning_at)
    elif type_of_list == 'for_the_future':
        form = BooksForTheFutureForm(name=book.name,
                                     author=book.author,
                                     link=book.link)
    return form


def fill_book(type_of_list, form):
    if type_of_list == 'already_read':
        book = AlreadyRead(name=form.name.data,
                           author=form.author.data,
                           link=form.link.data,
                           beginning_at=form.beginning_at.data,
                           ending_at=form.ending_at.data,
                           opinion_about=form.opinion_about.data,
                           user_id=current_user.id)
    elif type_of_list == 'in_the_process':
        book = InTheProcess(name=form.name.data,
                            author=form.author.data,
                            link=form.link.data,
                            beginning_at=form.beginning_at.data,
                            user_id=current_user.id)
    else:
        book = ForTheFuture(name=form.name.data,
                            author=form.author.data,
                            link=form.link.data,
                            user_id=current_user.id)
    return book
