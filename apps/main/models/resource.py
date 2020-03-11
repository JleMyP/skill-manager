from django.db import models

from utils.models import (
    CreatedAtMixin,
    IconMixin,
    LikeMixin,
    NameMixin,
    OrderedMixin,
)

__all__ = ['Resource', 'ResourceType', 'VolumeType']


class Resource(NameMixin,
               OrderedMixin,
               CreatedAtMixin,
               LikeMixin,
               IconMixin):
    description = models.TextField(
        verbose_name='Описание', null=True, blank=True,
    )
    parent = models.ForeignKey(
        verbose_name='Батя', to='self', on_delete=models.SET_NULL, null=True, blank=True,
    )
    type = models.ForeignKey(  # noqa: VNE003
        verbose_name='Тип ресурса', to='ResourceType', on_delete=models.SET_NULL, null=True,
    )
    volume_type = models.ForeignKey(
        verbose_name='Тип объема', to='VolumeType', on_delete=models.SET_NULL, null=True,
    )
    volume = models.FloatField(
        verbose_name='Объем', null=True, blank=True,
    )

    link = models.URLField(
        verbose_name='Ссыль', null=True, blank=True,
    )
    text = models.TextField(
        verbose_name='Текст', null=True, blank=True,
    )
    file = models.FileField(  # noqa: VNE002
        verbose_name='Файл', null=True, blank=True,
    )
    # image = models.ImageField(
    image = models.TextField(
        verbose_name='Картинка', null=True, blank=True,
    )
    raw_data = models.TextField(
        verbose_name='Сырые данные', null=True, blank=True,
    )
    imported_resource = models.OneToOneField(
        verbose_name='Импортированный ресурс', to='ImportedResource',
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name='resource',
    )
    tag_values = models.ManyToManyField(
        verbose_name='Метки со значениями', to='TagValue', blank=True,
    )

    planned_progress_points = models.FloatField(
        verbose_name='Планируемые очки прогресса', default=0,
    )
    difficulty_points = models.FloatField(  # complexity?
        verbose_name='Очки сложности', default=0,
    )

    class Meta:
        verbose_name = 'Ресурс'
        verbose_name_plural = 'Ресурсы'
        default_related_name = 'resources'

    def __str__(self):
        return f'({self.type.name}) {self.name}'


class ResourceType(NameMixin,
                   OrderedMixin):
    """Статья, текст, файл, книга, видеокурс, канал, заметка, git, тест, хабр и тд."""

    description = models.TextField(
        verbose_name='Описание', null=True, blank=True,
    )

    class Meta:
        verbose_name = 'Тип ресурса'
        verbose_name_plural = 'Типы ресурсов'
        default_related_name = 'resource_types'


class VolumeType(NameMixin,
                 OrderedMixin,
                 CreatedAtMixin):
    """Видосы, минуты, символы, ..."""

    class Meta:
        verbose_name = 'Тип объема'
        verbose_name_plural = 'Типы объема'
        default_related_name = 'volume_types'
