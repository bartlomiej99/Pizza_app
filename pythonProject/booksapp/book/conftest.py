import pytest
from bookapp.models import Book


@pytest.fixture
def test_book():
    link = 'http://books.google.com/books/' \
           'content?id=DqLPAAAAMAAJ&printsec' \
           '=frontcover&img=1&zoom=1&source=gbs_api'
    book = Book.objects.create(title='Harry Potter',
                               author='J.K. Rowling',
                               date_of_publication='2001',
                               isbn_number=1234567891234,
                               number_of_pages=478,
                               link_to_the_cover=link,
                               language='en')
    return book


@pytest.fixture
def test_second_book():
    link = 'http://books.google.pl/' \
           'books?id=FZa5NAEACAAJ&dq=Hobbit&hl=&cd=4&source=gbs_api'
    book = Book.objects.create(title='Henry',
                               author='Steve',
                               date_of_publication='2011',
                               isbn_number=1234567907654,
                               number_of_pages=342,
                               link_to_the_cover=link,
                               language='pl')
    return book
