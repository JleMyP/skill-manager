from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Folder, Progress, Remind, Resource, ResourceType, ImportedResource, VolumeType, Skill, Tag, TagValue, Task


class FolderInlineAdmin(admin.TabularInline):
    model = Folder
    list_display = ('id', 'parent', 'name', 'created_at', 'order_num', 'like', 'icon')
    extra = 0


@admin.register(Folder)
class FolderAdmin(VersionAdmin):
    list_display = ('id', 'parent', 'name', 'created_at', 'order_num', 'like', 'icon')
    search_fields = ('id', 'name')
    inlines = (FolderInlineAdmin,)


@admin.register(Progress)
class ProgressAdmin(VersionAdmin):
    list_display = ('id', 'created_at', 'task', 'resource', 'points', 'comment')
    search_fields = ('id',)


@admin.register(Remind)
class RemindAdmin(VersionAdmin):
    list_display = ('id', 'enabled', 'created_at', 'skill', 'task', 'resource', 'datetime',
                    'interval')
    search_fields = ('id',)


@admin.register(Resource)
class ResourceAdmin(VersionAdmin):
    list_display = ('id', 'parent', 'name', 'created_at', 'like', 'icon', 'type', 'volume_type',
                    'volume', 'planned_progress_points', 'difficulty_points')
    search_fields = ('id', 'name')


@admin.register(ResourceType)
class ResourceTypeAdmin(VersionAdmin):
    list_display = ('id', 'name', 'order_num')
    search_fields = ('id', 'name')


@admin.register(VolumeType)
class VolumeTypeAdmin(VersionAdmin):
    list_display = ('id', 'name', 'created_at', 'order_num')
    search_fields = ('id', 'name')


@admin.register(Tag)
class TagAdmin(VersionAdmin):
    list_display = ('id', 'name', 'created_at', 'order_num', 'like')
    search_fields = ('id', 'name')


@admin.register(TagValue)
class TagValueAdmin(VersionAdmin):
    list_display = ('id', 'tag', 'name', 'created_at', 'order_num')
    search_fields = ('id', 'name')


@admin.register(ImportedResource)
class ImportedResourceAdmin(VersionAdmin):
    list_display = ('id', 'name', 'provider', 'created_at', 'is_ignored', 'resource')
    list_filter = ('provider', 'is_ignored')
    search_fields = ('id', 'name')
