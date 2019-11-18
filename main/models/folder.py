from django.db import models

from utils.models import NameMixin, OrderedMixin, CreatedAtMixin, LikeMixin

__all__ = ['Folder']


class Folder(NameMixin, OrderedMixin, CreatedAtMixin, LikeMixin):
    parent = models.ForeignKey(
        verbose_name='Батя', to='self', null=True, blank=True,
    )
    icon = None

    class Meta:
        verbose_name = 'Папка'
        verbose_name_plural = 'Папки'
        default_related_name = 'folders'
