from django.db import models
from markdownx.models import MarkdownxField
from mptt.models import MPTTModel, TreeForeignKey

from utils.models import (
    CreatedAtMixin,
    IconMixin,
    LikeMixin,
    NameMixin,
    OrderedMixin,
)

__all__ = ['Skill']


class Skill(MPTTModel,
            NameMixin,
            CreatedAtMixin,
            OrderedMixin,
            LikeMixin,
            IconMixin):
    parent = TreeForeignKey(
        verbose_name='Батька', to='self', on_delete=models.SET_NULL,
        null=True, blank=True,
    )
    description = MarkdownxField(
        verbose_name='Описание',
    )
    folder = models.ForeignKey(
        verbose_name='Папка', to='Folder', blank=True,
        on_delete=models.PROTECT,
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
