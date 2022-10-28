import pytest
from photoapp.models import Photo


@pytest.fixture
def test_photo():
    photo = Photo.objects.create(
        album_id=1,
        id=2,
        title="reprehenderit est deserunt velit ipsam",
        url="https://via.placeholder.com/600/771796",
        width=600,
        height=600,
        color='771796')
    return photo


@pytest.fixture
def test_second_photo():
    photo = Photo.objects.create(
        album_id=1,
        id=14,
        title="est necessitatibus architecto ut laborum",
        url="https://via.placeholder.com/600/61a65",
        width=600,
        height=600,
        color='61a65')
    return photo
