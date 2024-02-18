#import all required libraries and modules
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime
import datetime

# creating an instance of SQLAlchemy and bind it to the Flask app:
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# define a constructor and a repr method for the class:
class Book(db.Model):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    author = Column(String(100), nullable=False)
    isbn = Column(String(13), unique=True, nullable=False)
    publication_year = Column(Integer, nullable=False)
    status = Column(String(10), default='available')
    check_out_date = Column(DateTime, nullable=True)
    due_date = Column(DateTime, nullable=True)
    issued_to = Column(String(100), nullable=True)

    def __init__(self, title, author, isbn, publication_year):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publication_year = publication_year

    def __repr__(self):
        return f'<Book {self.title} by {self.author}>'

# create the books table in the database by running the following command:
# db.create_all()

# ----------------------define the routers for endpoints--------------------
@app.route('/api/books', methods=['GET'])
def get_all_books():
    books = db.session.query(Book).all()
    books_list = [book.__dict__ for book in books]
    return jsonify({'code': 200, 'payload': books_list, 'success': True})

# ---second endpoint for adding new books------------------------
@app.route('/api/books', methods=['POST'])
def add_book():
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    isbn = data.get('isbn')
    publication_year = data.get('publication_year')
    if not title or not author or not isbn or not publication_year:
        return jsonify({'code': 422, 'error': 'Missing parameters', 'payload': {}, 'success': False})
    book = Book(title, author, isbn, publication_year)
    db.session.add(book)
    db.session.commit()
    return jsonify({'code': 200, 'payload': book.__dict__, 'success': True})

# ---third endpoint for updating books details------------------------
@app.route('/api/books/<id>', methods=['PUT'])
def update_book(id):
    book = db.session.query(Book).filter_by(id=id).first()
    if not book:
        return jsonify({'code': 404, 'error': 'Book not found', 'payload': {}, 'success': False})
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    isbn = data.get('isbn')
    publication_year = data.get('publication_year')
    status = data.get('status')
    check_out_date = data.get('check_out_date')
    due_date = data.get('due_date')
    issued_to = data.get('issued_to')
    if title:
        book.title = title
    if author:
        book.author = author
    if isbn:
        book.isbn = isbn
    if publication_year:
        book.publication_year = publication_year
    if status:
        book.status = status
    if check_out_date:
        book.check_out_date = datetime.datetime.strptime(check_out_date, '%Y-%m-%d')
    if due_date:
        book.due_date = datetime.datetime.strptime(due_date, '%Y-%m-%d')
    if issued_to:
        book.issued_to = issued_to
    db.session.commit()
    return jsonify({'code': 200, 'payload': book.__dict__, 'success': True})

# ---forth endpoint for deleting a book------------------------
@app.route('/api/books/<id>', methods=['DELETE'])
def delete_book(id):
    book = db.session.query(Book).filter_by(id=id).first()
    if not book:
        return jsonify({'code': 404, 'error': 'Book not found', 'payload': {}, 'success': False})
    db.session.delete(book)
    db.session.commit()
    return jsonify({'code': 200, 'message': f'Book {book.title} by {book.author} deleted', 'success': True})

# ---fivth endpoint searching for a book------------------------
@app.route('/api/books/search', methods=['GET'])
def search_books():
    title = request.args.get('title')
    author = request.args.get('author')
    publication_year = request.args.get('publication_year')
    if not title and not author and not publication_year:
        return jsonify({'code': 422, 'error': 'No search parameters', 'payload': {}, 'success': False})
    books = db.session.query(Book)
    if title:
        books = books.filter(or_(Book.title.like(f'%{title}%'), Book.title.like(f'%{title.lower()}%'), Book.title.like(f'%{title.upper()}%')))
    if author:
        books = books.filter(or_(Book.author.like(f'%{author}%'), Book.author.like(f'%{author.lower()}%'), Book.author.like(f'%{author.upper()}%')))
    if publication_year:
        books = books.filter(Book.publication_year == publication_year)
    books_list = [book.__dict__ for book in books.all()]
    return jsonify({'code': 200, 'payload': books_list, 'success': True})

# ------------------------------------------------------------------------------------------------






