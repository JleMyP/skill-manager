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

__all__ = ['Tag', 'TagValue']


class Tag(NameMixin,
          CreatedAtMixin,
          OrderedMixin,
          LikeMixin,
          IconMixin):
    TARGET_TYPE = IntFlag('Tag.TARGET_TYPE', 'FOLDER RESOURCE SKILL')
    ANY_TARGET = TARGET_TYPE.FOLDER | TARGET_TYPE.RESOURCE | TARGET_TYPE.SKILL

    color = ColorField(
        verbose_name='Цвет', null=True, blank=True,
    )
    target_type = IntFlagField(
        verbose_name='Тип цели', enum=TARGET_TYPE, default=int(ANY_TARGET),
    )

    class Meta:
        verbose_name = 'Метка'
        verbose_name_plural = 'Метки'
        default_related_name = 'tags'

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new:
            self.values.create(is_default=True)


class TagValue(NameMixin,
               CreatedAtMixin,
               OrderedMixin,
               IconMixin):
    """
    пример: метка 'ЯП', значение 'python'
    """
    DEFAULT_NAME = 'default'

    tag = models.ForeignKey(
        verbose_name='Метка', to='Tag', on_delete=models.CASCADE,
    )
    is_default = models.BooleanField(
        verbose_name='Значение по умолчанию', default=False,
    )

    def save(self, *args, **kwargs):
        if self._state.adding and self.is_default:
            self.name = self.DEFAULT_NAME
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Значение метки'
        verbose_name_plural = 'Значения меток'
        default_related_name = 'values'

    def __str__(self):
        if self.is_default:
            return str(self.tag)
        return f'{self.tag.name} : {self.name}'
