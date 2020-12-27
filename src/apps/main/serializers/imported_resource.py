from rest_framework import serializers

from ..models import ImportedResource

__all__ = ['ImportedResourceSerializer']


class ImportedResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportedResource
        exclude = ('raw_data',)
