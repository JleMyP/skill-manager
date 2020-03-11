from constance import config
from django.contrib.postgres.fields import JSONField, ArrayField


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
    raw_data = JSONField(
        verbose_name='Сырые данные', null=True, blank=True,
    )
    is_ignored = models.BooleanField(
        verbose_name='В игноре', default=False,
    )

    class Meta:
        verbose_name = 'Импортированный ресурс'
        verbose_name_plural = 'Импортированные ресурсы'
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
    short_name = models.CharField(
        verbose_name='Короткое название', max_length=255,
    )
    url = models.URLField(
        verbose_name='Ссыль на репу',
    )
    homepage = models.URLField(
        verbose_name='Домашняя страница', null=True, blank=True,
    )
    language = models.CharField(
        verbose_name='Язык', max_length=255, null=True, blank=True,
    )
    topics = ArrayField(
        verbose_name='Топики', base_field=models.CharField(
            max_length=255), default=list, blank=True,
    )
    from_user = models.CharField(
        verbose_name='Владелец закладки', max_length=255, null=True, blank=True,
    )

    class Meta:
        verbose_name = 'Импортированный ресурс (git)'
        verbose_name_plural = 'Импортированные ресурсы (git)'
        default_related_name = 'imported_resources'

    def create_resource(self) -> 'Resource':
        if self.is_ignored or hasattr(self, 'resource'):
            return self.resource

        from . import Resource, ResourceType, TagValue

        rt_pk = config.GIT_IMPORT_RESOURCE_TYPE
        rt = ResourceType.objects.get(pk=rt_pk)
        res = Resource.objects.create(
            type=rt,
            imported_resource=self,
            name=self.name,
            description=self.description,
            link=self.url,
        )

        tag_pk = config.GIT_IMPORT_TAG
        if tag_pk:
            tag_value = TagValue.objects.get(pk=tag_pk)
            res.tag_values.add(tag_value)

        # TODO: git tags?
        return res
