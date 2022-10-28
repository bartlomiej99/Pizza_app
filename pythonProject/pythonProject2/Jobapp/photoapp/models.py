from django.db import models


class Photo(models.Model):
    title = models.CharField(max_length=256, verbose_name='Title')
    id = models.IntegerField(primary_key=True, unique=True, verbose_name='Id')
    album_id = models.IntegerField(verbose_name='Album ID')
    width = models.IntegerField(verbose_name='Width')
    height = models.IntegerField(verbose_name='Height')
    color = models.CharField(max_length=6, verbose_name='Dominant color')
    url = models.URLField(max_length=256, verbose_name='Link to photo', null=True)

    def __str__(self):
        return self.title
