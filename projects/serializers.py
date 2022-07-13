from rest_framework import serializers
from projects.models import Keyword

class KeywordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Keyword
        fields = ('keyword','updated_at')