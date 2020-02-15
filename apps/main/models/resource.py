from django.db import models

from utils.models import NameMixin, OrderedMixin, CreatedAtMixin, LikeMixin, IconMixin

__all__ = ['Resource', 'ResourceType', 'VolumeType']


class Resource(NameMixin, OrderedMixin, CreatedAtMixin, LikeMixin, IconMixin):
    description = models.TextField(
        verbose_name='Описание',
    )
    parent = models.ForeignKey(
        verbose_name='Батя', to='self', on_delete=models.SET_NULL, null=True, blank=True,
    )
    type = models.ForeignKey(
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
        verbose_name='Текс', null=True, blank=True,
    )
    file = models.FileField(
        verbose_name='Файл', null=True, blank=True,
    )
    # image = models.ImageField(
    image = models.TextField(
        verbose_name='Картинка', null=True, blank=True,
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


class ResourceType(NameMixin, OrderedMixin):
    """
    статья, текст, файл, книга, видеокурс, канал, заметка, git, тест, хабр и тд
    """
    class Meta:
        verbose_name = 'Тип ресурса'
        verbose_name_plural = 'Типы ресурсы'
        default_related_name = 'resource_types'


class VolumeType(NameMixin, OrderedMixin, CreatedAtMixin):
    """
    видосы, минуты, символы, ...
    """
    class Meta:
        verbose_name = 'Тип объема'
        verbose_name_plural = 'Типы объема'
        default_related_name = 'volume_types'
