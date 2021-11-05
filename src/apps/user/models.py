from django.contrib.auth.models import AbstractUser
from django.db import models

__all__ = ['CustomUser']


class CustomUser(AbstractUser):
    middle_name = models.CharField(
        verbose_name='Отчество', max_length=150, blank=True,
    )

    def get_full_name(self) -> str:
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    def get_short_name(self) -> str:
        return f'{self.last_name} {self.first_name[:1]}.{self.middle_name[:1]}'

    def __str__(self) -> str:
        return self.get_full_name()
