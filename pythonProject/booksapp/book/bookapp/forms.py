import django.forms as forms
from .validators import validate_title,\
    validate_isbn_number,\
    validate_book_slug
from .models import Book


class BookSearchForm(forms.Form):
    title = forms.CharField(max_length=256, label='Title')
    author = forms.CharField(max_length=64, label='Author')
    language = forms.CharField(max_length=256, label='Language')
    date = forms.CharField(max_length=64, label='Date of publication')


class AddBookForm(forms.Form):
    title = forms.CharField(max_length=256, label='Title',
                            validators=[validate_title])
    author = forms.CharField(max_length=64, label='Author')
    date_of_publication = forms.CharField(max_length=64,
                                          label='Date of publication')
    isbn_number = forms.IntegerField(label='ISBN number',
                                     validators=[validate_isbn_number])
    number_of_pages = forms.IntegerField(label='Number of pages')
    link_to_the_cover = forms.URLField(label='Link to the cover',
                                       validators=[validate_book_slug])
    language = forms.CharField(max_length=256, label='Language of publication')


class DeleteBookForm(forms.Form):
    title = forms.ModelChoiceField(queryset=Book.objects.all(),
                                   required=True, label='Title')
    isbn_number = forms.IntegerField(label='ISBN number')


class EditBookForm(forms.Form):
    title = forms.ModelChoiceField(queryset=Book.objects.all(), label='Title')
    new_title = forms.CharField(max_length=256, label='Title',
                                validators=[validate_title])
    author = forms.CharField(max_length=64, label='Author')
    date_of_publication = forms.CharField(max_length=64,
                                          label='Date of publication')
    isbn_number = forms.IntegerField(label='ISBN number',
                                     validators=[validate_isbn_number])
    number_of_pages = forms.IntegerField(label='Number of pages')
    link_to_the_cover = forms.URLField(label='Link to the cover',
                                       validators=[validate_book_slug])
    language = forms.CharField(max_length=256, label='Language of publication')


class BookApiSearchForm(forms.Form):
    title = forms.CharField(max_length=256, label='Title')
    isbn_number = forms.IntegerField(label='ISBN number', required=False,
                                     validators=[validate_isbn_number])
