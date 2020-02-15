from django.db import models

from utils.models import CreatedAtMixin

__all__ = ['Remind']


class Remind(CreatedAtMixin):
    skill = models.ForeignKey(
        verbose_name='ЗУН', to='Skill', on_delete=models.CASCADE, null=True, blank=True,
    )
    task = models.ForeignKey(
        verbose_name='Задача', to='Task', on_delete=models.CASCADE, null=True, blank=True,
    )
    resource = models.ForeignKey(
        verbose_name='Ресурс', to='Resource', on_delete=models.CASCADE, null=True, blank=True,
    )
    datetime = models.DateTimeField(
        verbose_name='Дата-время срабатывания',
    )
    enabled = models.BooleanField(
        verbose_name='Включено', default=True,
    )
    interval = models.DurationField(
        verbose_name='Интервал повторения',
    )

    class Meta:
        verbose_name = 'Напоминание'
        verbose_name_plural = 'Напоминания'
        default_related_name = 'reminds'
