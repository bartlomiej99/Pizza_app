from django.contrib import admin
from django.urls import path
from bookapp.views import HomePageView, AddBookView,\
    BookSearchView, BookView, EditBookView, DeleteBookView,\
    BookFilterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view()),
    path('add-book/', AddBookView.as_view()),
    path('edit-book/', EditBookView.as_view()),
    path('delete-book/', DeleteBookView.as_view()),
    path('api/', BookSearchView.as_view()),
    path('api-view/', BookView.as_view()),
    path('api-filter/', BookFilterView.as_view()),
]
