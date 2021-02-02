from collections import OrderedDict

from django.apps import apps
from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer

from ..models import ImportedResource, ImportedResourceRepo

__all__ = ['ImportedResourceSerializer', 'ImportedResourceRepoSerializer',
           'ImportedResourcePolySerializer']


class ImportedResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportedResource
        exclude = ('raw_data',)


class ImportedResourceRepoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportedResourceRepo
        exclude = ('raw_data',)


class DetailsedSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        only = kwargs.pop('only', ())
        exclude = kwargs.pop('exclude', ())
        super().__init__(*args, kwargs)
        if only:
            allowed = set(only)
            existed = set(self.fields)
            for field in existed - allowed:
                self.fields.pop(field)
        for field in exclude:
            self.fields.pop(field, None)


class ImportedResourcePolySerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        ImportedResource: ImportedResourceSerializer,
        ImportedResourceRepo: ImportedResourceRepoSerializer,
    }

    def to_resource_type(self, model_or_instance):
        ptype = getattr(model_or_instance, 'ptype', None)
        if ptype:
            return apps.get_model(model_or_instance._meta.app_label, ptype)._meta.object_name
        return super().to_resource_type(model_or_instance)

    def to_representation(self, instance):
        """Группируем все специфичные поля в отдельный словарь."""
        serialized = super().to_representation(instance)
        type_specific = {}
        parent_fields = [field.name for field in ImportedResource._meta.fields]
        for field, value in serialized.items():
            if field not in parent_fields and field != 'resourcetype':
                type_specific[field] = value
        serialized = OrderedDict({key: value for key, value in serialized.items()
                                  if key in parent_fields or key == 'resourcetype'},
                                 type_specific=type_specific)
        return serialized
