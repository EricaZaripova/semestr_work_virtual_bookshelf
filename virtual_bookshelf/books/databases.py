from virtual_bookshelf import db
from books.models import AlreadyRead, InTheProcess, ForTheFuture, Quotes


def get_already_read_books(user_id):
    return db.session.query(AlreadyRead).filter(AlreadyRead.user_id == user_id).all()


def get_in_the_process_books(user_id):
    return db.session.query(InTheProcess).filter(InTheProcess.user_id == user_id).all()


def get_for_the_future_books(user_id):
    return db.session.query(ForTheFuture).filter(ForTheFuture.user_id == user_id).all()


def get_book_by_id(type_of_list, book_id):
    if type_of_list == 'already_read':
        table = AlreadyRead
    elif type_of_list == 'in_the_process':
        table = InTheProcess
    else:
        table = ForTheFuture
    return db.session.query(table).filter(table.id == book_id).first()


def get_quote_by_id(quote_id):
    return db.session.query(Quotes).filter(Quotes.id == quote_id).first()


def get_quotes_by_book_id(book_id):
    return db.session.query(Quotes).filter(Quotes.book_id == book_id).all()


def get_all_book(user_id):
    already_read_books = db.session.execute(f'SELECT name FROM already_read_books WHERE user_id = {user_id}').fetchall()
    in_the_process_books = db.session.execute(f'SELECT name FROM in_the_process_books WHERE user_id = {user_id}').fetchall()
    for_the_future_books = db.session.execute(f'SELECT name FROM for_the_future_books WHERE user_id = {user_id}').fetchall()
    return already_read_books+in_the_process_books+for_the_future_books
