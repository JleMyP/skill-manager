from django.db import models

from utils.models import NameMixin, CreatedAtMixin, OrderedMixin, LikeMixin, IconMixin

__all__ = ['Skill']


class Skill(NameMixin, CreatedAtMixin, OrderedMixin, LikeMixin, IconMixin):
    description = models.TextField(
        verbose_name='Описание',
    )
    folders = models.ManyToManyField(
        verbose_name='Папки', to='Folder', blank=True,
    )
    resources = models.ManyToManyField(
        verbose_name='Ресурсы', to='Resource', blank=True,
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
        verbose_name = 'ЗУН'
        verbose_name_plural = 'ЗУНы'
        default_related_name = 'skills'
