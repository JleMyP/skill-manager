from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Project, ProjectVariant, ProjectLink


class ProjectVariantAdminInline(VersionAdmin, admin.StackedInline):
    model = ProjectVariant
    extra = 0


class ProjectLinkAdminInline(VersionAdmin, admin.TabularInline):
    model = ProjectLink
    extra = 0


@admin.register(Project)
class ProjectAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'order_num', 'icon', 'like')
    search_fields = ('id', 'name')
    inlines = (ProjectVariant,)


@admin.register(ProjectVariant)
class ProjectVariantAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ('id', 'name', 'project', 'created_at', 'order_num', 'like')
    search_fields = ('id', 'name', 'project__name')
    inlines = (ProjectLink,)


@admin.register(ProjectLink)
class ProjectLinkAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ('id', 'project_variant', 'url')
    search_fields = ('id', 'project_variant__name', 'url')
