from django.test import TestCase
from .models import Photo
import pytest
# Create your tests here.


@pytest.mark.django_db
def test_create_photo_view(client):
    response = client.post('/photo-add/', {
        "album_id": 1,
        "id": 2,
        "title": "reprehenderit est deserunt velit ipsam",
        "url": "https://via.placeholder.com/600/771796",
        "width": 600,
        "height": 600,
        'color': '771796'})
    assert response.status_code == 302


@pytest.mark.django_db
def test_delete_photo_view(client, test_photo):
    response = client.post('/photo-delete/', {'title': [test_photo.title],
                                              'id': [test_photo.id]})
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_photo_view(client, test_photo, test_second_photo):
    photo = Photo.objects.create(
        title=test_second_photo.title,
        id=test_second_photo.id,
        album_id=test_second_photo.album_id,
        width=test_second_photo.width,
        height=test_second_photo.height,
        color=test_second_photo.color)
    response = client.post('photo-edit/', {
        'title': photo,
        'id': test_photo.id,
        'album_id': test_photo.album_id,
        'width': test_photo.width,
        'height': test_photo.height,
        'color': test_photo.color})
    assert response.status_code == 200


class PhotoSearchTitleTest(TestCase):
    @pytest.mark.django_db
    def test_photo_search_title(self):
        data = {'title': "harum dicta similique quis dolore earum ex qui"}
        response = self.client.get('/api-filter/', data=data)
        self.assertEqual(response.status_code, 200)


class PhotoSearchIdTest(TestCase):
    @pytest.mark.django_db
    def test_photo_search_id(self):
        data = {'id': 13}
        response = self.client.get('/api-filter/', data=data)
        self.assertEqual(response.status_code, 200)
