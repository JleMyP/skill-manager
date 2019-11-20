from enum import IntFlag, EnumMeta

from django.db import models
from django.db.models import Lookup

__all__ = ['ColorField', 'IntFlagField']


class ColorField(models.PositiveIntegerField):
    pass


class IntFlagField(models.PositiveSmallIntegerField):
    """
    Пример:

    class SomeModel(models.Model):
        COLORS = IntFlag('Colors', 'RED GREEN BLUE')
        colors = IntFlagField(enum=COLORS, default=COLORS.RED)

    имеющюе красный. зеленый и синий - не важно
    SomeModel.objects.filter(colors__has_bit=SomeModel.COLORS.RED)

    имеющие и красный и зеленый. синий - не важно
    SomeModel.objects.filter(colors__has_bit=SomeModel.COLORS.RED | SomeModel.COLORS.GREEN)

    имеющие красный или зеленый. синий - не важно
    SomeModel.objects.filter(colors__any_bit=SomeModel.COLORS.RED | SomeModel.COLORS.GREEN)
    """
    # TODO:
    #  доступ к перечислению через <ModelClass>.<FieldName>.enum
    #  свой класс перечисления со свойством all

    def __init__(self, enum, enum_name=None, *args, **kwargs):
        self.enum = enum if isinstance(enum, EnumMeta) else IntFlag(enum_name or 'flag field', enum)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        # TODO: замутить
        kwargs['enum'] = [flag.name for flag in self.enum]
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection):
        if value is not None:
            return self.enum(value)

    def to_python(self, value):
        value = super().to_python(value)
        if isinstance(value, self.enum):
            return value
        if value is not None:
            return self.enum(value)


@IntFlagField.register_lookup
class HasBitLookup(Lookup):
    lookup_name = 'has_bit'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        return '%s & %s = %s' % (lhs, rhs, rhs), rhs_params + rhs_params


@IntFlagField.register_lookup
class AnyBitLookup(Lookup):
    lookup_name = 'any_bit'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        return '%s & %s > 0' % (lhs, rhs), rhs_params + rhs_params
