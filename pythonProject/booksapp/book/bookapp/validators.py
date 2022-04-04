from django.core.exceptions import ValidationError
from .models import Book


def validate_title(title):
    if Book.objects.filter(title=title):
        raise ValidationError('Book with this title exists!')


def validate_isbn_number(isbn_number):
    if Book.objects.filter(isbn_number=isbn_number):
        raise ValidationError('Book with this number exists!')


def validate_book_slug(link_to_the_cover):
    if Book.objects.filter(link_to_the_cover=link_to_the_cover):
        raise ValidationError('Book with this link exists!')
