from django.db import models

__all__ = ['CreatedAtMixin', 'NameMixin', 'OrderedMixin', 'LikeMixin', 'IconMixin']


class MixinBase(models.Model):
    class Meta:
        abstract = True


class CreatedAtMixin(MixinBase):
    created_at = models.DateTimeField(
        verbose_name='Дата-время создания', auto_now_add=True,
    )


class NameMixin(MixinBase):
    name = models.CharField(
        verbose_name='Название', max_length=50,
    )

    def __str__(self):
        return self.name


class OrderedManager(models.Manager):
    @property
    def ordered_desc(self):
        return self.get_queryset().order_by('-order_num')

    @property
    def ordered_asc(self):
        return self.get_queryset().order_by('order_num')


class OrderedMixin(MixinBase):
    order_num = models.PositiveIntegerField(
        verbose_name='Очередь', default=0,
    )

    objects = OrderedManager()


class LikeMixin(MixinBase):
    like = models.BooleanField(
        verbose_name='Лайк', default=False,
    )


class IconMixin(MixinBase):
    icon = models.CharField(
        verbose_name='Иконка', max_length=15, null=True, blank=True,
    )
