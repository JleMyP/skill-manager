import json

from constance import config
from django.db import models
from polymorphic.models import PolymorphicModel

from utils.models import (
    CreatedAtMixin,
    NameMixin,
)


__all__ = ['ImportedResource', 'ImportedResourceRepo']



class ImportedResource(CreatedAtMixin, NameMixin, PolymorphicModel):
    description = models.TextField(
        verbose_name='Описание', null=True, blank=True,
    )
    raw_data = models.TextField(
        verbose_name='Сырые данные', null=True, blank=True,
    )
    is_ignored = models.BooleanField(
        verbose_name='В игноре', default=False,
    )

    class Meta:
        verbose_name = 'Импортированный ресурс (git)'
        verbose_name_plural = 'Импортированные ресурсы (git)'
        default_related_name = 'imported_resources'

    def ignore(self):
        if self.is_ignored:
            return

        self.is_ignored = True
        self.save(update_fields=('is_ignored',))

    def unignore(self):
        if not self.is_ignored:
            return

        self.is_ignored = False
        self.save(update_fields=('is_ignored',))


class ImportedResourceRepo(ImportedResource):
    def create_resource(self):
        if self.is_ignored or self.resource:
            return

        from . import Resource, ResourceType, TagValue

        raw_data = json.loads(self.raw_data)
        rt_pk = config.GIT_IMPORT_RESOURCE_TYPE
        rt = ResourceType.objects.get(pk=rt_pk)
        res = Resource.objects.create(
            type=rt,
            imported_resource=self,
            name=self.name,
            description=self.description,
            link=raw_data['url'],
        )

        tag_pk = config.GIT_IMPORT_TAG
        if tag_pk:
            tag_value = TagValue.objects.get(pk=tag_pk)
            res.tag_values.add(tag_value)

        # TODO: git tags?
        return res
