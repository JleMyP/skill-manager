from django.db import models

__all__ = ['CreatedAtMixin', 'NameMixin', 'OrderedMixin', 'LikeMixin', 'IconMixin']


class CreatedAtMixin(models.Model):
    created_at = models.DateTimeField(
        verbose_name='Дата-время создания', auto_now_add=True,
    )

    class Meta:
        abstract = True


class NameMixin(models.Model):
    name = models.CharField(
        verbose_name='Название', max_length=250,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class OrderedManager(models.Manager):
    @property
    def ordered_desc(self):
        return self.get_queryset().order_by('-order_num')

    @property
    def ordered_asc(self):
        return self.get_queryset().order_by('order_num')


class OrderedMixin(models.Model):
    order_num = models.PositiveIntegerField(
        verbose_name='Очередь', default=0,
    )

    class Meta:
        abstract = True

    objects = OrderedManager()


class LikeMixin(models.Model):
    like = models.BooleanField(
        verbose_name='Лайк', default=False,
    )

    class Meta:
        abstract = True


class IconMixin(models.Model):
    icon = models.CharField(
        verbose_name='Иконка', max_length=15, null=True, blank=True,
    )

    class Meta:
        abstract = True
