from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, DestroyAPIView,\
    UpdateAPIView
from .models import Photo
from rest_framework import generics, filters
from .forms import PhotoApiSearchForm, PhotoAddForm,\
    PhotoDeleteForm, PhotoEditForm, PhotoSearchForm
import json
from .serializers import PhotoSerializer
import requests
import urllib.request
from PIL import Image


class HomePageView(View):
    """ Home page shows all links to other views,
    method POST search for books in database"""
    def get(self, request):
        form = PhotoSearchForm()
        photo = Photo.objects.all().order_by('id')
        return render(request, 'homepage.html', {
            'form': form, 'photos': photo})

    def post(self, request):
        form = PhotoSearchForm(request.POST)
        if form.is_valid():
            book = Photo.objects.filter(
                title=form.cleaned_data['title'],
                id=form.cleaned_data['id'],)
            return render(request, 'homepage.html', {'books': book})
        else:
            return render(request, 'homepage.html', {'form': form})


class PhotoListView(View):
    def get(self, request):
        form = PhotoApiSearchForm()
        return render(request, 'photolist.html', {'form': form})

    def post(self, request):
        form = PhotoApiSearchForm(request.POST)
        if form.is_valid():
            try:
                title = form.cleaned_data['title']
                album_id = form.cleaned_data['album_id']
                response = requests.get(
                    f"https://jsonplaceholder.typicode.com/photos/"
                    f"{album_id}+intitle:{title}"
                ).text
                response_info = json.loads(response)
                album_id = response_info['albumId']
                id_no = response_info['id']
                title = response_info['title']
                url = response_info['url']
                width = response_info['url']
                width_no = [n for n in width if n.isdigit()]
                digit = ''.join(width_no)
                Photo.objects.create(title=title,
                                     album_id=album_id,
                                     id=id_no,
                                     url=url,
                                     width=digit,
                                     height=digit)
                return render(request, 'photolist.html', {'form': form})
            except KeyError:
                return render(request, 'photolist.html', {'form': form})


# class CreatePhotoView(View):
#     def get(self, request):
#         form = PhotoAddForm()
#         return render(request, 'photocreate.html', {'form': form})
#
#     def post(self, request):
#         form = PhotoAddForm(request.POST)
#         if form.is_valid():
#             Photo.objects.create(title=form.cleaned_data['title'],
#                                  id=form.cleaned_data['id'],
#                                  album_id=form.cleaned_data['album_id'],
#                                  width=form.cleaned_data['width'],
#                                  height=form.cleaned_data['height'],
#                                  color=form.cleaned_data['color'],
#                                  url=form.cleaned_data['url'])
#             return redirect('/')
#         else:
#             return render(request, 'photocreate.html', {'form': form})


# class DeletePhotoView(View):
#     def get(self, request):
#         form = PhotoDeleteForm()
#         return render(request, 'photodelete.html', {'form': form})
#
#     def post(self, request):
#         form = PhotoDeleteForm(request.POST)
#         if form.is_valid():
#             photo = Photo.objects.filter(title=form.cleaned_data['title'],
#                                          id=form.cleaned_data['id'])
#             photo.delete()
#             return redirect('/')
#         else:
#             return render(request, 'photodelete.html', {'form': form})


# class EditPhotoView(View):
#     def get(self, request):
#         form = PhotoEditForm()
#         return render(request, 'photoedit.html', {'form': form})
#
#     def post(self, request):
#         form = PhotoEditForm(request.POST)
#         if form.is_valid():
#             photo = Photo.objects.get(title=form.cleaned_data['title'])
#             photo.title = form.cleaned_data['new_title']
#             photo.id = form.cleaned_data['id']
#             photo.album_id = form.cleaned_data['album_id']
#             photo.width = form.cleaned_data['width']
#             photo.height = form.cleaned_data['height']
#             photo.color = form.cleaned_data['color']
#             photo.url = form.cleaned_data['url']
#             photo.save()
#             return redirect('/')
#         else:
#             return render(request, 'photoedit.html', {'form': form})


@api_view(['GET'])
def get_image(request):
    response = requests.get('https://jsonplaceholder.typicode.com/photos')
    if request.method == 'GET':
        return HttpResponse(response.content, content_type="image/jpeg")


class ImageImportView(View):
    def get(self, request):
        form = PhotoApiSearchForm()
        return render(request, 'photolist.html', {'form': form})

    def post(self, request):
        form = PhotoApiSearchForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            album_id = form.cleaned_data['album_id']
            response = requests.get(
                f"https://jsonplaceholder.typicode.com/photos/"
                f"{album_id}+intitle:{title}"
            ).text
            response_info = json.loads(response)
            url = response_info['url']
            urllib.request.urlretrieve(url)
            img = Image.open(url)
            return render(request, 'photolist.html', {'form': form, 'img': img})


class PhotoSearchView(generics.ListAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'album_id', 'url']


class PhotoCreateView(CreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def post(self, request, *args, **kwargs):
        form = PhotoAddForm(request.POST)
        if form.is_valid():
            Photo.objects.create(title=form.cleaned_data['title'],
                                 id=form.cleaned_data['id'],
                                 album_id=form.cleaned_data['album_id'],
                                 width=form.cleaned_data['width'],
                                 height=form.cleaned_data['height'],
                                 color=form.cleaned_data['color'],
                                 url=form.cleaned_data['url'])
            return redirect('/')
        else:
            return render(request, 'photocreate.html', {'form': form})


class PhotoEditView(DestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def delete(self, request, *args, **kwargs):
        form = PhotoDeleteForm(request.POST)
        if form.is_valid():
            photo = Photo.objects.filter(title=form.cleaned_data['title'],
                                         id=form.cleaned_data['id'])
            photo.delete()
            return redirect('/')
        else:
            return render(request, 'photodelete.html', {'form': form})


class PhotoDeleteView(UpdateAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def update(self, request, *args, **kwargs):
        form = PhotoEditForm(request.POST)
        if form.is_valid():
            photo = Photo.objects.get(title=form.cleaned_data['title'])
            photo.title = form.cleaned_data['new_title']
            photo.id = form.cleaned_data['id']
            photo.album_id = form.cleaned_data['album_id']
            photo.width = form.cleaned_data['width']
            photo.height = form.cleaned_data['height']
            photo.color = form.cleaned_data['color']
            photo.url = form.cleaned_data['url']
            photo.save()
            return redirect('/')
        else:
            return render(request, 'photoedit.html', {'form': form})
