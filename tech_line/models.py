from django.db import models

from utils.models import NameMixin, OrderedMixin, IconMixin, CreatedAtMixin

__all__ = ['TechLine', 'TechLineElement']


class TechLine(NameMixin, CreatedAtMixin, IconMixin):
    description = models.TextField(
        verbose_name='Описание',
    )

    class Meta:
        verbose_name = 'Линия технологий'
        verbose_name_plural = 'Линии технологий'
        default_related_name = 'tech_lines'


class TechLineElement(NameMixin, CreatedAtMixin, OrderedMixin):
    tech_line = models.ForeignKey(
        verbose_name='Линия технологий', to='TechLine', on_delete=models.CASCADE,
    )
    skills = models.ManyToManyField(
        verbose_name='ЗУНы', to='main.Skill', blank=True,
    )
    weight = models.FloatField(
        verbose_name='Вес-значимость',
    )

    class Meta:
        verbose_name = 'Элемент линии технологий'
        verbose_name_plural = 'Элементы линий технологий'
        default_related_name = 'tech_line_elements'
