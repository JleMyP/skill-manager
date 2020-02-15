from django.db import models

from utils.models import CreatedAtMixin

__all__ = ['Progress']


class Progress(CreatedAtMixin):
    task = models.ForeignKey(
        verbose_name='Задача', to='Task', on_delete=models.CASCADE, null=True, blank=True,
    )
    resource = models.ForeignKey(
        verbose_name='Ресурс', to='Resource', on_delete=models.CASCADE, null=True, blank=True,
    )
    points = models.FloatField(
        verbose_name='Очки',
    )
    comment = models.TextField(
        verbose_name='Комментарий', null=True, blank=True,
    )

    class Meta:
        verbose_name = 'Прогресс'
        verbose_name_plural = 'Прогресс'
        default_related_name = 'progress'
