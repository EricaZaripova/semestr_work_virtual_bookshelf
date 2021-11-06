from virtual_bookshelf import db


class AlreadyRead(db.Model):
    __tablename__ = 'already_read_books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    author = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String())
    beginning_at = db.Column(db.DateTime(), nullable=False)
    ending_at = db.Column(db.DateTime(), nullable=False)
    opinion_about = db.Column(db.Text())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

    def __repr__(self):
        return f'{self.id}, {self.user_id}'


class InTheProcess(db.Model):
    __tablename__ = 'in_the_process_books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    author = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String())
    beginning_at = db.Column(db.DateTime(), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

    def __repr__(self):
        return f'{self.id}, {self.user_id}'


class ForTheFuture(db.Model):
    __tablename__ = 'for_the_future_books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    author = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

    def __repr__(self):
        return f'{self.id}, {self.user_id}'


class Quotes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(), nullable=False)
    speaker = db.Column(db.String())
    place = db.Column(db.String())

    book_id = db.Column(db.Integer, db.ForeignKey('already_read_books.id', ondelete='CASCADE'))
