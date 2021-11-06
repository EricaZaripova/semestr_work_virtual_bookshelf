from flask import render_template

from virtual_bookshelf import app


@app.route('/')
def main():
    return render_template('main.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
