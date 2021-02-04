from rest_framework import serializers

from ..models import Tag, TagValue

__all__ = ['TagSerializer']


class TagValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagValue
        exclude = ('tag',)


class TagSerializer(serializers.ModelSerializer):
    values = TagValueSerializer(many=True)

    class Meta:
        model = Tag
        fields = '__all__'
