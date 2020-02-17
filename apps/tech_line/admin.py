from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import TechLine, TechLineElement


class ElementAdminInline(VersionAdmin, admin.TabularInline):
    model = TechLineElement
    extra = 0


@admin.register(TechLine)
class TechLineAdmin(VersionAdmin):
    list_display = ('id', 'name', 'created_at', 'icon')
    search_fields = ('id', 'name')
    inlines = (ElementAdminInline,)
    date_hierarchy = 'created_at'
    actions_on_bottom = True


@admin.register(TechLineElement)
class TechLineElementAdmin(VersionAdmin):
    list_display = ('id', 'name', 'created_at', 'order_num', 'tech_line', 'weight')
    search_fields = ('id', 'name', 'tech_line__name')
    date_hierarchy = 'created_at'
    actions_on_bottom = True
