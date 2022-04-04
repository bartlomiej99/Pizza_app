from django.test import TestCase
from .models import Book
import pytest


@pytest.mark.django_db
def test_book_add(client):
    link = 'http://books.google.com/books/' \
           'content?id=DqLPAAAAMAAJ&printsec=frontcover' \
           '&img=1&zoom=1&source=gbs_api'
    client.post('/add-book/', {'title': 'Harry Potter',
                               'author': 'Tolkien',
                               'date_of_publication': '2006',
                               'isbn_number': 2004314566123,
                               'number_of_pages': 267,
                               'link_to_the_cover': link,
                               'language': 'en'})
    assert Book.objects.count() == 1


@pytest.mark.django_db
def test_book_add_without_param(client):
    link = 'http://books.google.com/books/' \
           'content?id=DqLPAAAAMAAJ&printsec=frontcover&' \
           'img=1&zoom=1&source=gbs_api'
    client.post('/add-book/', {'title': 'Harry Potter',
                               'date_of_publication': '2006',
                               'isbn_number': 2004314566123,
                               'number_of_pages': 267,
                               'link_to_the_cover': link,
                               'language': 'en'})
    assert Book.objects.count() == 0


@pytest.mark.django_db
def test_book_delete(client, test_book):
    response = client.post('/delete-book/', {
        'title': [test_book.title],
        'isbn_number': [test_book.isbn_number]})
    assert response.status_code == 200


@pytest.mark.django_db
def test_bok_edit(client, test_second_book, test_book):
    book = Book.objects.create(
        title=test_second_book.title,
        author=test_second_book.author,
        date_of_publication=test_second_book.date_of_publication,
        isbn_number=test_second_book.isbn_number,
        number_of_pages=test_second_book.number_of_pages,
        link_to_the_cover=test_second_book.link_to_the_cover,
        language=test_second_book.language)
    response = client.post('/edit-book/', {
        'title': book,
        'new_title': test_book.title,
        'author': test_book.author,
        'date_of_publication': test_book.date_of_publication,
        'isbn_number': test_book.isbn_number,
        'number_of_pages': test_book.number_of_pages,
        'link_to_the_cover': test_book.link_to_the_cover,
        'language': test_book.language})
    assert response.status_code == 200


@pytest.mark.django_db
def test_book_api_add(client):
    response = client.post('/api-view/', {
        'title': 'Hobbit czyli tam i z powrotem',
        'isbn_number': 8324403876
    })
    assert response.status_code == 200


class BookSearchTitleTest(TestCase):
    @pytest.mark.django_db
    def test_book_search_title(self):
        data = {'title': 'Harry Potter'}
        response = self.client.get('/api/', data=data)
        self.assertEqual(response.status_code, 200)


class BookSearchAuthorTest(TestCase):
    @pytest.mark.django_db
    def test_book_search_author(self):
        data = {'author': 'J.K Rowling'}
        response = self.client.get('/api/', data=data)
        self.assertEqual(response.status_code, 200)


class BookSearchLanguageTest(TestCase):
    @pytest.mark.django_db
    def test_book_search_author(self):
        data = {'language': 'en'}
        response = self.client.get('/api/', data=data)
        self.assertEqual(response.status_code, 200)


class BookSearchIsbnTest(TestCase):
    @pytest.mark.django_db
    def test_book_search_author(self):
        data = {'isbn_number': 123136347473}
        response = self.client.get('/api-filter/', data=data)
        self.assertEqual(response.status_code, 200)


class BookSearchDateTest(TestCase):
    @pytest.mark.django_db
    def test_book_search_author(self):
        data = {'date_of_publication': '2009-02-12'}
        response = self.client.get('/api-filter/', data=data)
        self.assertEqual(response.status_code, 200)


class BookSearchPageTest(TestCase):
    @pytest.mark.django_db
    def test_book_search_author(self):
        data = {'number_of_pages': 465}
        response = self.client.get('/api-filter/', data=data)
        self.assertEqual(response.status_code, 200)
