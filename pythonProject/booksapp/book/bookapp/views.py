from django.shortcuts import render, redirect
from django.views import View
from .models import Book
from .forms import BookSearchForm, AddBookForm, BookApiSearchForm, \
    DeleteBookForm, EditBookForm
from .serializers import BookSerializer
from rest_framework import generics, filters
import json
import requests


class HomePageView(View):
    """ Home page shows all links to other views,
    method POST search for books in database"""
    def get(self, request):
        form = BookSearchForm()
        books = Book.objects.all().order_by('id')
        return render(request, 'homepage.html', {'form': form, 'books': books})

    def post(self, request):
        form = BookSearchForm(request.POST)
        if form.is_valid():
            book = Book.objects.filter(
                title=form.cleaned_data['title'],
                author=form.cleaned_data['author'],
                language=form.cleaned_data['language'],
                date_of_publication=form.cleaned_data['date'])
            return render(request, 'homepage.html', {'books': book})
        else:
            return render(request, 'homepage.html', {'form': form})


class AddBookView(View):
    """ Method GET shows empty form and method POST,
    saves all the information about new book and adds it to the database"""
    def get(self, request):
        form = AddBookForm()
        return render(request, 'addbook.html', {'form': form})

    def post(self, request):
        form = AddBookForm(request.POST)
        if form.is_valid():
            Book.objects.create(
                title=form.cleaned_data['title'],
                author=form.cleaned_data['author'],
                date_of_publication=form.cleaned_data['date_of_publication'],
                isbn_number=form.cleaned_data['isbn_number'],
                number_of_pages=form.cleaned_data['number_of_pages'],
                link_to_the_cover=form.cleaned_data['link_to_the_cover'],
                language=form.cleaned_data['language'])
            return redirect('/')
        else:
            return render(request, 'addbook.html', {'form': form})


class DeleteBookView(View):
    """ Entering by method GET show empty form,
    Method POST takes model that we picked and deletes it from database"""
    def get(self, request):
        form = DeleteBookForm()
        return render(request, 'deletebook.html', {'form': form})

    def post(self, request):
        form = DeleteBookForm(request.POST)
        if form.is_valid():
            book = Book.objects.filter(
                title=form.cleaned_data['title'],
                isbn_number=form.cleaned_data['isbn_number'])
            book.delete()
            return redirect('/')
        return render(request, 'deletebook.html', {'form': form})


class EditBookView(View):
    """ Method Get shows empty form,
    Method POST pick the model and edit it's value that we choose"""
    def get(self, request):
        form = EditBookForm()
        return render(request, 'editbook.html', {'form': form})

    def post(self, request):
        form = EditBookForm(request.POST)
        if form.is_valid():
            book = Book.objects.get(title=form.cleaned_data['title'])
            book.title = form.cleaned_data['new_title']
            book.author = form.cleaned_data['author']
            book.date_of_publication = form.cleaned_data['date_of_publication']
            book.isbn_number = form.cleaned_data['isbn_number']
            book.number_of_pages = form.cleaned_data['number_of_pages']
            book.link_to_the_cover = form.cleaned_data['link_to_the_cover']
            book.language = form.cleaned_data['language']
            book.save()
            return redirect('/')
        else:
            return render(request, 'editbook.html', {'form': form})


class BookView(View):
    """ Method GET show empty form,
    in method POST we type the title and ISBN number
    then it searches in google API Books,
    and gives as the data, then we search by dict and tabs
    and if all information are included
    method create new model and save it to the database"""
    def get(self, request):
        form = BookApiSearchForm()
        return render(request, 'bookapiview.html', {'form': form})

    def post(self, request):
        form = BookApiSearchForm(request.POST)
        if form.is_valid():
            try:
                title = form.cleaned_data['title']
                isbn_number = form.cleaned_data['isbn_number']
                response = requests.get(
                    f"https://www.googleapis.com/"
                    f"books/v1/volumes?q={isbn_number}+intitle:{title}"
                ).text
                response_info = json.loads(response)
                var = response_info['items'][0]['volumeInfo']
                title1 = var['title']
                authors = ""
                for a in var['authors']:
                    authors += a
                publication_date = var['publishedDate']
                isbn_no = var['industryIdentifiers'][0]['identifier']
                page_count = var['pageCount']
                link = var['imageLinks']['thumbnail']
                language = var['language']
                Book.objects.create(
                    title=title1, author=authors,
                    date_of_publication=publication_date,
                    isbn_number=isbn_no,
                    number_of_pages=page_count, link_to_the_cover=link,
                    language=language)
                return render(request, 'bookapiview.html', {'form': form})
            except KeyError:
                return render(request, 'bookapiview.html', {
                    'form': form,
                    'info': 'One of parameters is not included in the API'})


class BookSearchView(generics.ListAPIView):
    """ """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author', 'date_of_publication', 'language']


class BookFilterView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['date_of_publication', 'number_of_pages', 'isbn_number']
