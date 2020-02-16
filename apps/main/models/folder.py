from django.db import models

from utils.models import (
    NameMixin,
    OrderedMixin,
    CreatedAtMixin,
    LikeMixin,
    IconMixin
)

__all__ = ['Folder']


class Folder(NameMixin,
             OrderedMixin,
             CreatedAtMixin,
             LikeMixin,
             IconMixin):
    parent = models.ForeignKey(
        verbose_name='Батя', to='self', on_delete=models.SET_NULL, null=True, blank=True,
    )

    class Meta:
        verbose_name = 'Папка'
        verbose_name_plural = 'Папки'
        default_related_name = 'folders'
