import django.forms as forms
from .models import Photo
from .validators import validate_title


class PhotoSearchForm(forms.Form):
    title = forms.CharField(max_length=256, label='Title')
    id = forms.IntegerField(label='Id')


class PhotoApiSearchForm(forms.Form):
    title = forms.CharField(max_length=256, label='Title')
    album_id = forms.IntegerField(label='Album ID')
    url = forms.URLField(label='Link to photo')


class PhotoAddForm(forms.Form):
    title = forms.CharField(max_length=256,
                            label='Title',
                            validators=[validate_title])
    id = forms.IntegerField(label='Id')
    album_id = forms.IntegerField(label='Album ID')
    width = forms.IntegerField(label='Width')
    height = forms.IntegerField(label='Height')
    color = forms.CharField(max_length=6, label='Dominant color')
    url = forms.URLField(max_length=256, label='Link to photo')


class PhotoDeleteForm(forms.Form):
    itle = forms.CharField(max_length=256, label='Title')
    id = forms.IntegerField(label='Id')


class PhotoEditForm(forms.Form):
    title = forms.ModelChoiceField(queryset=Photo.objects.all(), label='Title')
    new_title = forms.CharField(max_length=256, label='Title')
    id = forms.IntegerField(label='Id')
    album_id = forms.IntegerField(label='Album ID')
    width = forms.IntegerField(label='Width')
    height = forms.IntegerField(label='Height')
    color = forms.CharField(max_length=6, label='Dominant color')
    url = forms.URLField(max_length=256, label='Link to photo')
