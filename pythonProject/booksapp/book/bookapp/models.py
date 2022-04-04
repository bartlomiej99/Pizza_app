from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=256, verbose_name='Title')
    author = models.CharField(max_length=256, verbose_name='Author')
    date_of_publication = models.CharField(max_length=64,
                                           verbose_name='Date of publication')
    isbn_number = models.BigIntegerField(verbose_name='ISBN number')
    number_of_pages = models.IntegerField(verbose_name='Number of pages')
    link_to_the_cover = models.URLField(verbose_name='Link to the cover')
    language = models.CharField(max_length=256,
                                verbose_name='Language of publication')

    def __str__(self):
        return self.title
