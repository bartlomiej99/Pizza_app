from django.core.exceptions import ValidationError
from .models import Photo


def validate_title(title):
    if Photo.objects.filter(title=title):
        raise ValidationError('Photo with this title exsist!')
