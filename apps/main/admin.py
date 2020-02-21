from autocompletefilter.admin import AutocompleteFilterMixin
from autocompletefilter.filters import AutocompleteListFilter
from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import (
    Folder,
    ImportedResource,
    Progress,
    Remind,
    Resource,
    ResourceType,
    Skill,
    Tag,
    TagValue,
    Task,
    VolumeType,
)


class FolderInlineAdmin(admin.TabularInline):
    model = Folder
    list_display = ('id', 'name', 'parent', 'created_at', 'order_num', 'like', 'icon')
    extra = 0


@admin.register(Folder)
class FolderAdmin(VersionAdmin):
    list_display = ('id', 'name', 'parent', 'created_at', 'order_num', 'like', 'icon')
    list_editable = ('order_num',)
    search_fields = ('id', 'name')
    inlines = (FolderInlineAdmin,)
    date_hierarchy = 'created_at'
    actions_on_bottom = True


@admin.register(Progress)
class ProgressAdmin(VersionAdmin):
    list_display = ('id', 'created_at', 'task', 'resource', 'points', 'comment')
    search_fields = ('id',)
    date_hierarchy = 'created_at'
    actions_on_bottom = True


@admin.register(Remind)
class RemindAdmin(VersionAdmin):
    list_display = ('id', 'enabled', 'created_at', 'skill', 'task', 'resource', 'datetime',
                    'interval')
    search_fields = ('id',)
    date_hierarchy = 'created_at'
    actions_on_bottom = True


@admin.register(Resource)
class ResourceAdmin(AutocompleteFilterMixin, VersionAdmin):
    list_display = ('id', 'name', 'parent', 'created_at', 'like', 'icon', 'type', 'volume_type',
                    'volume', 'planned_progress_points', 'difficulty_points')
    search_fields = ('id', 'name')
    list_display_links = ('id', 'name')
    list_filter = (
        'like',
        ('type', AutocompleteListFilter),
        ('volume_type', AutocompleteListFilter),
        ('parent', AutocompleteListFilter),
    )
    date_hierarchy = 'created_at'
    actions_on_bottom = True


@admin.register(ResourceType)
class ResourceTypeAdmin(VersionAdmin):
    list_display = ('id', 'name', 'order_num')
    list_display_links = ('id', 'name')
    list_editable = ('order_num',)
    search_fields = ('id', 'name')
    actions_on_bottom = True


@admin.register(ImportedResource)
class ImportedResourceAdmin(VersionAdmin):
    list_display = ('id', 'name', 'provider', 'created_at', 'is_ignored', 'resource')
    list_filter = ('provider', 'is_ignored')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')
    date_hierarchy = 'created_at'
    actions_on_bottom = True


@admin.register(VolumeType)
class VolumeTypeAdmin(VersionAdmin):
    list_display = ('id', 'name', 'created_at', 'order_num')
    list_display_links = ('id', 'name')
    list_editable = ('order_num',)
    search_fields = ('id', 'name')
    date_hierarchy = 'created_at'
    actions_on_bottom = True


@admin.register(Tag)
class TagAdmin(VersionAdmin):
    list_display = ('id', 'name', 'created_at', 'order_num', 'like')
    list_display_links = ('id', 'name')
    list_filter = ('like',)
    list_editable = ('order_num', 'like')
    search_fields = ('id', 'name')
    date_hierarchy = 'created_at'
    actions_on_bottom = True


@admin.register(TagValue)
class TagValueAdmin(VersionAdmin):
    list_display = ('id', 'tag', 'name', 'is_default', 'created_at', 'order_num')
    list_filter = ('is_default',)
    list_editable = ('order_num',)
    search_fields = ('id', 'name')
    date_hierarchy = 'created_at'
    actions_on_bottom = True


@admin.register(Skill)
class SkillAdmin(VersionAdmin):
    list_display = ('id', 'name', 'parent', 'created_at', 'planned_progress_points', 'difficulty_points')
    list_filter = (
        ('parent', AutocompleteListFilter),
    )
    list_editable = ('planned_progress_points', 'difficulty_points')
    search_fields = ('id', 'name')
    date_hierarchy = 'created_at'
    actions_on_bottom = True


@admin.register(Task)
class TaskAdmin(VersionAdmin):
    list_display = ('id', 'name', 'created_at', 'order_num', 'like', 'skill', 'project',
                    'planned_progress_points', 'difficulty_points', 'completed')
    list_filter = ('completed', 'like')
    list_editable = ('order_num',)
    date_hierarchy = 'created_at'
    actions_on_bottom = True
