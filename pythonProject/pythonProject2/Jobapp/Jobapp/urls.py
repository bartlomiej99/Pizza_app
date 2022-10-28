"""Jobapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from photoapp.views import PhotoListView, PhotoSearchView,\
    HomePageView, PhotoCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view()),
    path('api-view/', PhotoListView.as_view()),
    # path('photo-add/', CreatePhotoView.as_view()),
    # path('photo-edit/', EditPhotoView.as_view()),
    # path('photo-delete/', DeletePhotoView.as_view()),
    path('api-filter/', PhotoSearchView.as_view()),
    path('api/', PhotoCreateView.as_view()),
]
