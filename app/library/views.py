import flask, imghdr, os
from werkzeug.utils import secure_filename
from . import library
from .. import db
from .forms import (RegisterBookForm, RegisterBookCategoryForm, RegisterAuthorForm, 
        RegisterPublisherForm, AssignBookAuthorForm, UpdateBookCoverForm, 
        UpdateProfileImageForm)

from ..models import (book, book_category, related_book, author_assignment,
        publisher_contact, publisher, book_assignment, book_author)


def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)

    if not format:
        return None

    return '.' + (format if format == 'jpeg' else 'jpg')


@library.route('/')
@library.route('/homepage')
def homepage():
    return flask.render_template('library/homepage.html')


@library.route('/register_book', methods = ['GET', 'POST'])
def register_book():
    form = RegisterBookForm()

    categories = book_category.query.order_by(book_category.category_name.asc()).all()
    publishers = publisher.query.order_by(publisher.publisher_name.desc()).all()

    form.book_category.choices = [((category.category_id), (category.category_name)) 
            for category in categories]
    form.publisher_id.choices = [((publisher.publisher_id), (publisher.publisher_name)) 
            for publisher in publishers]

    if form.validate_on_submit():
        Book = book(
                title = form.title.data,
                year_of_production = form.year_of_production.data,
                publisher_id = form.publisher_id.data,
                book_category_id = form.book_category.data
                )
        db.session.add(Book)
        db.session.commit()

        flask.flash(f'{form.title.data} registered successfully.')
        return flask.redirect(flask.url_for('library.register_book'))

    return flask.render_template('library/register_book.html', form = form)


@library.route('register_book_category', methods = ['GET', 'POST'])
def register_book_category():
    form = RegisterBookCategoryForm()

    if form.validate_on_submit():
        Category = book_category(
                category_name = form.category_name.data
                )
        db.session.add(Category)
        db.session.commit()

        flask.flash(f'{form.category_name.data} added successfully.')
        return flask.redirect(flask.url_for('library.register_book_category'))

    return flask.render_template('library/register_book_category.html', form = form)


@library.route('register_author', methods = ['GET', 'POST'])
def register_author():
    form = RegisterAuthorForm()

    if form.validate_on_submit():
        Author = book_author(
                first_name = form.first_name.data,
                middle_name = form.middle_name.data,
                last_name = form.last_name.data,
                gender = form.gender.data,
                email_address = form.email_address.data,
                phone_no = form.phone_no.data,
                residential_address = form.residential_address.data,
                )
        db.session.add(Author)
        db.session.commit()

        flask.flash(f'{form.first_name.data} {form.middle_name.data} {form.last_name.data} registered successfully.')
        return flask.redirect(flask.url_for('library.register_author'))

    return flask.render_template('library/register_author.html', form = form)


@library.route('register_publisher', methods = ['GET', 'POST'])
def register_publisher():
    form = RegisterPublisherForm()

    if form.validate_on_submit():
        Publisher = publisher(
                publisher_name = form.publisher_name.data,
                location = form.location.data
                )
        db.session.add(Publisher)
        db.session.commit()

        flask.flash(f"{form.publisher_name.data} added successfully.")
        return flask.redirect(flask.url_for('library.register_publisher'))

    return flask.render_template('library/register_publisher.html', form = form)


@library.route('view_authors')
def view_all_authors():
    authors = book_author.query.order_by(book_author.first_name.asc()).all()
    return flask.render_template('library/view_all_authors.html', authors = authors)


@library.route('view_books')
def view_all_books():
    page = flask.request.args.get('page', 1, type = int)
    pagination = book.query.join(publisher, publisher.publisher_id == book.publisher_id)\
            .join(book_category, book_category.category_id == book.book_category_id)\
            .add_columns(
                    book.book_id,
                    book.title,
                    publisher.publisher_id,
                    publisher.publisher_name,
                    book_category.category_id,
                    book_category.category_name
                    ).order_by(book.title.asc())\
    .paginate(page, per_page = flask.current_app.config['FLASKY_POSTS_PER_PAGE'], 
            error_out = False)
    books = pagination.items

    return flask.render_template('library/view_all_books.html', books = books, 
            pagination = pagination)


@library.route('view_all_categories')
def view_all_categories():
    categories = book_category.query.order_by(book_category.category_name.asc()).all()
    return flask.render_template('library/view_all_categories.html', 
            categories = categories)

@library.route('view_all_publishers')
def view_all_publishers():
    page = flask.request.args.get('page', 1, type = int)
    pagination = publisher.query.order_by(publisher.publisher_name.asc())\
            .paginate(page, per_page = flask.current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out = False)
    publishers = pagination.items
    return flask.render_template('library/view_all_publishers.html', 
            publishers = publishers, pagination = pagination)


@library.route('/publisher_profile/<publisher_id>', methods = ['GET'])
def publisher_profile(publisher_id):
    Publisher = publisher.query.filter_by(publisher_id = publisher_id).first_or_404()
    page = flask.request.args.get('page', 1, type = int)

    pagination = book.query.filter_by(publisher_id = Publisher.publisher_id)\
            .join(book_category, book_category.category_id == book.book_category_id)\
            .add_columns(
                    book.book_id,
                    book.title,
                    book.status,
                    book.year_of_production,
                    book_category.category_id,
                    book_category.category_name
                    ).order_by(book.book_id.asc())\
            .paginate(page, per_page = flask.current_app.config['FLASKY_POSTS_PER_PAGE'], 
            error_out = False)

    books = pagination.items

    return flask.render_template('library/publisher_profile.html', publisher = Publisher, 
            books = books, pagination = pagination)

@library.route('/category_profile/<int:category_id>')
def category_profile(category_id):
    Category = book_category.query.filter_by(category_id = category_id).first_or_404()

    page = flask.request.args.get('page', 1, type = int)
    pagination = book.query.filter_by(book_category_id = category_id)\
            .order_by(book.title.asc()).paginate(page = page, error_out = False, 
                    per_page = flask.current_app.config['FLASKY_POSTS_PER_PAGE'])

    books = pagination.items

    return flask.render_template('library/category_profile.html', books = books, 
            category = Category, pagination = pagination)


@library.route('/book_profile/<int:book_id>')
def book_profile(book_id):
    Book = book.query.filter_by(book_id = book_id)\
            .join(book_category, book_category.category_id == book.book_category_id)\
            .join(publisher, publisher.publisher_id == book.publisher_id)\
            .first_or_404()

    authors = author_assignment.query.filter_by(book_id = Book.book_id)\
            .join(book_author, book_author.author_id == author_assignment.author_id)\
            .add_columns(
                    book_author.author_id,
                    book_author.first_name,
                    book_author.middle_name,
                    book_author.last_name
                    ).order_by(book_author.first_name.asc()).all()

    return flask.render_template('library/book_profile.html', authors = authors, 
            book = Book)


@library.route('/assign_author/<book_id>', methods = ['GET', 'POST'])
def assign_author(book_id):
    form = AssignBookAuthorForm()

    authors = book_author.query.order_by(book_author.first_name.asc()).all()

    form.author_id.choices = [((author.author_id), (author.first_name + ' ' + 
        author.middle_name + ' ' + author.last_name)) for author in authors]

    if form.validate_on_submit():
        Author_Assignment = author_assignment(
                author_id = form.author_id.data,
                book_id = book_id
                )
        db.session.add(Author_Assignment)
        db.session.commit()

        return flask.redirect(flask.url_for('library.book_profile', book_id = book_id))

    return flask.render_template('library/assign_author.html', form = form)

@library.route('/update_book_cover/<int:book_id>', methods = ['GET', 'POST'])
def update_book_cover(book_id):
    Book = book.query.filter_by(book_id = book_id).first_or_404()

    form = UpdateBookCoverForm()

    if form.validate_on_submit():
        uploaded_file = form.file.data
        filename = secure_filename(uploaded_file.filename)

        if filename != '':
            file_ext = os.path.splitext(filename)[1]

            if file_ext not in flask.current_app.config['UPLOAD_EXTENSIONS'] or \
                    file_ext != validate_image(uploaded_file.stream):
                        return 'Invalid Image', 400
            
            uploaded_file.save(os.path.join(
                flask.current_app.config['LIBRARY_UPLOAD_PATH'], filename))


        Book.image = filename
        db.session.add(Book)
        db.session.commit()

        return flask.redirect(flask.url_for('library.book_profile', book_id = book_id))

    return flask.render_template('library/update_book_cover.html', form = form)


@library.route('/update_publisher_profile_image/<int:publisher_id>', 
        methods = ['GET', 'POST'])
def update_publisher_profile_image(publisher_id):
    Publisher = publisher.query.filter_by(publisher_id = publisher_id).first_or_404()

    form = UpdateProfileImageForm()

    if form.validate_on_submit():
        uploaded_file = form.file.data
        filename = secure_filename(uploaded_file.filename)

        if filename != '':
            file_ext = os.path.splitext(filename)[1]

            if file_ext not in flask.current_app.config['UPLOAD_EXTENSIONS'] or \
                    file_ext != validate_image(uploaded_file.stream):
                        return 'Invalid Image', 400

            uploaded_file.save(os.path.join(
                flask.current_app.config['LIBRARY_UPLOAD_PATH'], 'publishers', filename))

        Publisher.image = filename
        db.session.add(Publisher)
        db.session.commit()

        return flask.redirect(
                flask.url_for('library.publisher_profile', publisher_id = publisher_id))
        
    return flask.render_template('library/update_publisher_profile_image.html', 
            form = form)


@library.route('/update_author_profile_image/<int:author_id>', methods = ['GET', 'POST'])
def update_author_profile_image(author_id):
    Author = book_author.query.filter_by(author_id = author_id).first_or_404()

    form = UpdateProfileImageForm()

    if form.validate_on_submit():
        uploaded_file = form.file.data
        filename = secure_filename(uploaded_file.filename)

        if filename != '':
            file_ext = os.path.splitext(filename)[1]

            if file_ext not in flask.current_app.config['UPLOAD_EXTENSIONS'] or \
                    file_ext != validate_image(uploaded_file.stream):
                        return 'Invalid Image', 400

            uploaded_file.save(os.path.join(
                flask.current_app.config['LIBRARY_UPLOAD_PATH'], 'authors', filename))

        Author.associated_image = filename
        db.session.add(Author)
        db.session.commit()

        return flask.redirect(
                flask.url_for('library.book_author_profile', author_id = author_id))

    return flask.render_template('library/update_author_profile_image.html', form = form)


@library.route('/book_author_profile/<int:author_id>')
def book_author_profile(author_id):
    author = book_author.query.filter_by(author_id = author_id).first_or_404()

    books = author_assignment.query.filter_by(author_id = author_id)\
            .join(book, book.book_id == author_assignment.book_id)\
            .add_columns(
                    book.book_id,
                    book.title,
                    book.image).order_by(book.title.asc()).all()

    return flask.render_template('library/book_author_profile.html', author = author, 
            books = books)
