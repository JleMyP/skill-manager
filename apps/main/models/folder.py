from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from utils.models import (
    CreatedAtMixin,
    IconMixin,
    LikeMixin,
    NameMixin,
    OrderedMixin,
)

__all__ = ['Folder']


class Folder(MPTTModel,
             NameMixin,
             OrderedMixin,
             CreatedAtMixin,
             LikeMixin,
             IconMixin):
    parent = TreeForeignKey(
        verbose_name='Батя', to='self', on_delete=models.SET_NULL, null=True, blank=True,
    )

    class Meta:
        verbose_name = 'Папка'
        verbose_name_plural = 'Папки'
        default_related_name = 'folders'
