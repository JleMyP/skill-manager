from django.contrib.admin import site
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, Permission
from reversion.admin import VersionAdmin
from reversion.models import Revision, Version

from .models import CustomUser


class VersionedUserAdmin(VersionAdmin, UserAdmin):
    fieldsets = (
        (None, {
            'fields': ('username', 'password'),
        }),
        ('Персональная информация', {
            'fields': (('first_name', 'last_name', 'middle_name'), 'email'),
        }),
        ('Права', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',),
        }),
        ('Даты', {
            'fields': (('last_login', 'date_joined'),),
            'classes': ('collapse',),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'middle_name',
                    'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'first_name', 'last_name', 'middle_name', 'email')
    change_form_template = 'loginas/change_form.html'


class VersionedGroupAdmin(VersionAdmin, GroupAdmin):
    pass


site.register(CustomUser, VersionedUserAdmin)
site.unregister(Group)
site.register(Group, VersionedGroupAdmin)
site.register(Permission)
site.register(Revision)
site.register(Version)
