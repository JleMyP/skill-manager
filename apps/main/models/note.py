from django.db import models
from markdownx.models import MarkdownxField

from utils.models import (
    CreatedAtMixin,
)

__all__ = ['Note']


class Note(CreatedAtMixin):
    description = MarkdownxField(
        verbose_name='Описание',
    )

    skills = models.ManyToManyField(
        verbose_name='ЗУНы', to='Skill', blank=True,
    )
    resources = models.ManyToManyField(
        verbose_name='Ресурсы', to='Resource', blank=True,
    )
    tag_values = models.ManyToManyField(
        verbose_name='Метки со значениями', to='TagValue', blank=True,
    )

    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'
        default_related_name = 'notes'
