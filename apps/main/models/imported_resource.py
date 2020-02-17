from django.db import models

from utils.models import (
    CreatedAtMixin,
    NameMixin,
)


__all__ = ['ImportedResource']


class ImportedResource(CreatedAtMixin, NameMixin):
    class Provider(models.IntegerChoices):
        GITHUB = (1, 'GitHub')
        CHROME = (2, 'Chrome')
        VK = (3, 'VK')

    provider = models.PositiveIntegerField(
        verbose_name='Провайдер', choices=Provider.choices,
    )
    description = models.TextField(
        verbose_name='Описание', null=True, blank=True,
    )
    raw_data = models.TextField(
        verbose_name='Сырые данные', null=True, blank=True,
    )
    is_ignored = models.BooleanField(
        verbose_name='В игноре', default=False,
    )

    class Meta:
        verbose_name = 'Импортированный ресурс'
        verbose_name_plural = 'Импортированные ресурсы'
        default_related_name = 'imported_resources'

    def ignore(self):
        if self.is_ignored:
            return

        self.is_ignored = True
        self.save(update_fields=('is_ignored',))

    def unignore(self):
        if not self.is_ignored:
            return

        self.is_ignored = False
        self.save(update_fields=('is_ignored',))
