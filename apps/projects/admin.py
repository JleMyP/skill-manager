from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Project, ProjectVariant, ProjectLink


class ProjectVariantAdminInline(admin.StackedInline):
    model = ProjectVariant
    extra = 0


class ProjectLinkAdminInline(admin.TabularInline):
    model = ProjectLink
    extra = 0


@admin.register(Project)
class ProjectAdmin(VersionAdmin):
    list_display = ('id', 'name', 'created_at', 'order_num', 'icon', 'like')
    list_editable = ('order_num',)
    search_fields = ('id', 'name')
    inlines = (ProjectVariantAdminInline,)
    date_hierarchy = 'created_at'
    actions_on_bottom = True


@admin.register(ProjectVariant)
class ProjectVariantAdmin(VersionAdmin):
    list_display = ('id', 'name', 'project', 'created_at', 'order_num', 'like')
    list_editable = ('order_num',)
    search_fields = ('id', 'name', 'project__name')
    inlines = (ProjectLinkAdminInline,)
    date_hierarchy = 'created_at'
    actions_on_bottom = True


@admin.register(ProjectLink)
class ProjectLinkAdmin(VersionAdmin):
    list_display = ('id', 'project_variant', 'url')
    search_fields = ('id', 'project_variant__name', 'url')
    actions_on_bottom = True
