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
        verbose_name='Тип цели', enum=TARGET_TYPE, default=ANY_TARGET,
    )
    simple = models.BooleanField(
        verbose_name='Простая (без значений)', default=True,
    )
    additional_info = None

    class Meta:
        verbose_name = 'Метка'
        verbose_name_plural = 'Метки'
        default_related_name = 'tags'

    def save(self, *args, **kwargs):
        # TODO: через self._state зырить
        super().save(*args, **kwargs)
        if not self.pk and self.simple:
            self.values.create(name='simple')


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

    def __str__(self):
        if self.tag.simple:
            return str(self.tag)
        return f'{self.tag.name} : {self.name}'
