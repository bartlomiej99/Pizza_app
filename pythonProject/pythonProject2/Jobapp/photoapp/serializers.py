from rest_framework import serializers


class PhotoSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=256, label='Title')
    id = serializers.IntegerField(label='Id')
    album_id = serializers.IntegerField(label='Album ID')
    width = serializers.IntegerField(label='Width')
    height = serializers.IntegerField(label='Height')
    color = serializers.CharField(max_length=6, label='Dominant color')
