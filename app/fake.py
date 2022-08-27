import faker
from random import randint
from . import db
from .models import (book_category, publisher)
from sqlalchemy.exc import IntegrityError


def start():
    print("starting computation...")


def finish():
    print("finished with status : done")


def create_book_categories():
    start()
    categories_list = [
            'Academic and Education', 
            'Biography', 
            'Children and Youth', 
            'Fiction and Literature', 
            'Lifestyle', 
            'Politics and Laws', 
            'Science and Research', 
            'Technology', 
            'Religion', 
            'Personal Growth', 
            'Health and Fitness', 
            'Environment', 
            'Business and Career', 
            'Art'
            ]

    for item in categories_list:
        Category = book_category(category_name = item)
        db.session.add(Category)
    db.session.commit()
    finish()


def create_publishers():
    start()
    publishers = [
            ('Southern Adventist University Printing Press', '102200 Pennyslavania, USA'),
            ('Packt Publishers - Birmingham', 
            'Birmingham, Mumbai - Livery Place, 35 Livery Street, Birmimgham, BB2PB, UK'),
            ("Simon & Schuster Children's Publishing Division", 
                '1230 Avenue of the Americas, New York, New York 100200'),
            ("TutorialsPoint PVT Ltd", "Mumbai, India")
            ]

    for item in publishers:
        Publisher = publisher(
                publisher_name = item[0],
                location = item[1]
                )
        db.session.add(Publisher)
    db.session.commit()
    finish()

