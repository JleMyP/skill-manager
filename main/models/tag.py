from random import randrange as rnd
from django.db import models

from utils.models import NameMixin, CreatedAtMixin, OrderedMixin, LikeMixin, ColorField
 
__all__ = ['Tag']


class Tag(NameMixin, CreatedAtMixin, OrderedMixin, LikeMixin):
    FOLDER = 1
    RESOURCE = 2
    SKILL = 4
    
    color = ColorField(
        verbose_name='Цвет',
    )
    icon = None
    target_type = models.PositiveIntegerField(
        verbose_name='Тип цели', default=FOLDER | RESOURCE | SKILL,
    )

    class Meta:
        verbose_name = 'Метка'
        verbose_name_plural = 'Метки'
        default_related_name = 'tags'


class TagValue(NameMixin, CreatedAtMixin, OrderedMixin):
    """
    пример: метка 'ЯП', значение 'python'
    """

    tag = models.ForeignKey(
        verbose_name='Метка', to='Tag',
    )
    icon = None

    class Meta:
        verbose_name = 'Значение метки'
        verbose_name_plural = 'Значения меток'
        default_related_name = 'values'
