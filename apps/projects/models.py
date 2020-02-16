from django.db import models

from utils.models import (
    NameMixin,
    OrderedMixin,
    CreatedAtMixin,
    LikeMixin,
    IconMixin,
)

__all__ = ['Project', 'ProjectVariant', 'ProjectLink']


class Project(NameMixin,
              OrderedMixin,
              CreatedAtMixin,
              IconMixin,
              LikeMixin):
    description = models.TextField(
        verbose_name='Описание',
    )

    skills = models.ManyToManyField(
        verbose_name='ЗУНы', to='main.Skill', blank=True,
    )
    resources = models.ManyToManyField(
        verbose_name='Ресурсы', to='main.Resource', blank=True,
    )
    tag_values = models.ManyToManyField(
        verbose_name='Метки со значениями', to='main.TagValue', blank=True,
    )

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        default_related_name = 'projects'


class ProjectVariant(NameMixin,
                     OrderedMixin,
                     CreatedAtMixin,
                     LikeMixin):
    project = models.ForeignKey(
        verbose_name='Проект', to='Project', on_delete=models.CASCADE,
    )
    description = models.TextField(
        verbose_name='Описание',
    )

    skills = models.ManyToManyField(
        verbose_name='ЗУНы', to='main.Skill', blank=True,
    )
    resources = models.ManyToManyField(
        verbose_name='Ресурсы', to='main.Resource', blank=True,
    )
    tag_values = models.ManyToManyField(
        verbose_name='Метки со значениями', to='main.TagValue', blank=True,
    )

    class Meta:
        verbose_name = 'Вариант проекта'
        verbose_name_plural = 'Варианты проектов'
        default_related_name = 'project_variants'


class ProjectLink(models.Model):
    project_variant = models.ForeignKey(
        verbose_name='Вариант проекта', to='ProjectVariant', on_delete=models.CASCADE,
    )
    url = models.URLField(
        verbose_name='Ссыль',
    )

    class Meta:
        verbose_name = 'Ссылка на проект'
        verbose_name_plural = 'Ссылки на проект'
        default_related_name = 'project_links'
