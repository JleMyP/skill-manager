from rest_framework import serializers

from ..models import ImportedResource

__all__ = ['ImportedResourceSerializer']


class ImportedResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportedResource
        fields = '__all__'
