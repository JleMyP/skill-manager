from rest_framework import serializers
from rest_framework_serializer_extensions.serializers import SerializerExtensionsMixin

from apps.main.models import Folder


class FolderSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = '__all__'
