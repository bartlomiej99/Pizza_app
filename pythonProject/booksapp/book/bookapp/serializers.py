from rest_framework import serializers


class BookSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=256, label='Title')
    author = serializers.CharField(max_length=64, label='Author')
    date_of_publication = serializers.CharField(label='Date of publication')
    isbn_number = serializers.IntegerField(label='ISBN number')
    number_of_pages = serializers.IntegerField(label='Number of pages')
    link_to_the_cover = serializers.URLField(label='Link to the cover')
    language = serializers.CharField(max_length=256,
                                     label='Language of publication')
