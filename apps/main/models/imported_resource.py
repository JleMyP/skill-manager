from django.contrib.postgres.fields import ArrayField
from django.db import models
from polymorphic.models import PolymorphicManager, PolymorphicModel
from polymorphic.query import PolymorphicQuerySet

from utils.models import CreatedAtMixin, NameMixin

__all__ = ['ImportedResource', 'ImportedResourceRepo']


class ImportedResourceQuerySet(PolymorphicQuerySet):
    def ignore(self):
        return self.update(is_ignored=True)
    ignore.queryset_only = True
    ignore.alters_data = True

    def unignore(self):
        return self.update(is_ignored=False)
    unignore.queryset_only = True
    unignore.alters_data = True


class ImportedResource(CreatedAtMixin, NameMixin, PolymorphicModel):
    description = models.TextField(
        verbose_name='Описание', null=True, blank=True,
    )
    raw_data = models.JSONField(
        verbose_name='Сырые данные', null=True, blank=True,
    )
    is_ignored = models.BooleanField(
        verbose_name='В игноре', default=False,
    )

    objects = PolymorphicManager.from_queryset(ImportedResourceQuerySet)()

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
