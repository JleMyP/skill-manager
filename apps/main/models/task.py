from django.db import models

from utils.models import NameMixin, OrderedMixin, CreatedAtMixin, LikeMixin

__all__ = ['Task']


class Task(NameMixin, OrderedMixin, CreatedAtMixin, LikeMixin):
    skill = models.ForeignKey(
        verbose_name='ЗУН', to='Skill', on_delete=models.CASCADE, null=True, blank=True,
    )
    project = models.ForeignKey(
        verbose_name='Проект', to='projects.Project', on_delete=models.CASCADE, null=True, blank=True,
    )

    parent = models.ForeignKey(
        verbose_name='Батя', to='self', on_delete=models.SET_NULL, null=True, blank=True,
    )
    description = models.TextField(
        verbose_name='Описание',
    )

    planned_progress_points = models.FloatField(
        verbose_name='Планируемые очки прогресса', default=0,
    )
    difficulty_points = models.FloatField(  # complexity?
        verbose_name='Очки сложности', default=0,
    )
    competed = models.BooleanField(
        verbose_name='Завершена', default=False,
    )

    resources = models.ManyToManyField(
        verbose_name='Ресурсы', to='Resource', blank=True,
    )
    tag_values = models.ManyToManyField(
        verbose_name='Метки со значениями', to='TagValue', blank=True,
    )

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        default_related_name = 'tasks'
