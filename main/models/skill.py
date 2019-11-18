from django.db import models

from utils.models import NameMixin, CreatedAtMixin, OrderedMixin, LikeMixin

__all__ = ['Skill']


class Skill(NameMixin, CreatedAtMixin, OrderedMixin, LikeMixin):
    description = models.TextField(
        verbose_name='Описание',
    )
    icon = None
    folders = models.ManyToMany(
        verbose_name='Папки', to='Folder', blank=True,
    )
    resources = models.ManyToMany(
        verbose_name='Ресурсы', to='Resource', blank=True,
    )
    tag_values = models.ManyToMany(
        verbose_name='Метки со значениями', to='TagValue', blank=True,
    )
    planned_progress_points = models.FloatField(
        verbose_name='Планируемые очки прогресса', default=0,
    )
    difficulty_points = models.FloatField(
        verbose_name='Очки сложности', default=0,
    )

    class Meta:
        verbose_name = 'ЗУН'
        verbose_name_plural = 'ЗУНы'
        default_related_name = 'skills'
