from enum import IntFlag

from django.db import models

from utils.fields import ColorField, IntFlagField
from utils.models import (
    NameMixin,
    CreatedAtMixin,
    OrderedMixin,
    LikeMixin,
    IconMixin,
)

__all__ = ['Tag']


class Tag(NameMixin,
          CreatedAtMixin,
          OrderedMixin,
          LikeMixin,
          IconMixin):
    TARGET_TYPE = IntFlag('Tag.TARGET_TYPE', 'FOLDER RESOURCE SKILL')
    ANY_TARGET = TARGET_TYPE.FOLDER | TARGET_TYPE.RESOURCE | TARGET_TYPE.SKILL

    color = ColorField(
        verbose_name='Цвет',
    )
    target_type = IntFlagField(
        verbose_name='Тип цели', enum=TARGET_TYPE, default=ANY_TARGET,
    )
    additional_info = None

    class Meta:
        verbose_name = 'Метка'
        verbose_name_plural = 'Метки'
        default_related_name = 'tags'


class TagValue(NameMixin,
               CreatedAtMixin,
               OrderedMixin,
               IconMixin):
    """
    пример: метка 'ЯП', значение 'python'
    """

    tag = models.ForeignKey(
        verbose_name='Метка', to='Tag', on_delete=models.CASCADE,
    )
    additional_info = None

    class Meta:
        verbose_name = 'Значение метки'
        verbose_name_plural = 'Значения меток'
        default_related_name = 'values'
