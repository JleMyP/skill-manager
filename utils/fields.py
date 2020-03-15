from enum import IntFlag

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
    #  в contribute_to_class можно привязаться к модели и сделать <ModelClass>.<FieldName>_ENUM
    #  свой класс перечисления со свойством all
    #  админковый виджет как для m2m

    def __init__(self, enum, *args, enum_name: str = None, **kwargs):
        if isinstance(enum, list):
            enum = IntFlag(enum_name, enum)
        self.enum = enum
        self.enum_name = enum.__name__
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        # TODO: замутить работоспособно
        #   либо списка во входном параметре не должно быть
        #     и класс перечисления всегда предопределен
        #   либо собирать класс перечисления на ходу
        #     никакого переиспользования даже в пределах класса
        #     и не оч понятно, как адекватно указывать default
        if isinstance(self.enum, list):
            kwargs['enum'] = self.enum
        else:
            kwargs['enum'] = [flag.name for flag in self.enum]
        kwargs['enum_name'] = self.enum_name
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
        return f'{lhs} & {rhs} = {rhs}', rhs_params + rhs_params


@IntFlagField.register_lookup
class AnyBitLookup(Lookup):
    lookup_name = 'any_bit'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        return f'{lhs} & {rhs} > 0', rhs_params + rhs_params
