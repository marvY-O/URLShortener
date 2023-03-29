from rest_framework import serializers
from .models import URL

class dbSerializer(serializers.ModelSerializer):
    class Meta:
        model=URL
        fields=('uid','longURL', 'shortURL')

class shortURLResponseSerializer(serializers.Serializer):
    shortURL = serializers.CharField(max_length = 100)
    longURL = serializers.CharField(max_length = 2048)