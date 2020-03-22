from autocompletefilter.admin import AutocompleteFilterMixin
from autocompletefilter.filters import AutocompleteListFilter
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django_object_actions import DjangoObjectActions
from mptt.admin import MPTTModelAdmin

from polymorphic.admin import (
    PolymorphicParentModelAdmin,
    PolymorphicChildModelAdmin,
    PolymorphicChildModelFilter,
)
from reversion.admin import VersionAdmin

from apps.main.models import (
    Folder,
    ImportedResource,
    ImportedResourceRepo,
    Note,
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
from apps.main.import_providers import github


class FolderInlineAdmin(admin.TabularInline):
    model = Folder
    list_display = ('id', 'name', 'parent', 'created_at', 'order_num', 'like', 'icon')
    extra = 0


@admin.register(Folder)
class FolderAdmin(MPTTModelAdmin, AutocompleteFilterMixin, VersionAdmin):
    list_display = ('id', 'name', 'parent', 'created_at', 'order_num', 'like', 'icon')
    list_editable = ('order_num',)
    list_filter = (
        ('parent', AutocompleteListFilter),
    )
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
class ResourceAdmin(MPTTModelAdmin, AutocompleteFilterMixin, VersionAdmin):
    list_display = ('id', 'name', 'parent', 'created_at', 'like', 'icon', 'type', 'volume_type',
                    'volume', 'planned_progress_points', 'difficulty_points')
    search_fields = ('id', 'name')
    list_display_links = ('id', 'name')
    list_filter = (
        'like',
        ('type', AutocompleteListFilter),
        ('volume_type', AutocompleteListFilter),
        ('parent', AutocompleteListFilter),
        ('tag_values', AutocompleteListFilter),
        ('tag_values__tag', AutocompleteListFilter),
    )
    date_hierarchy = 'created_at'
    filter_horizontal = ('tag_values',)
    actions_on_bottom = True


@admin.register(ResourceType)
class ResourceTypeAdmin(VersionAdmin):
    list_display = ('id', 'name', 'order_num')
    list_display_links = ('id', 'name')
    list_editable = ('order_num',)
    search_fields = ('id', 'name')
    actions_on_bottom = True


@admin.register(VolumeType)
class VolumeTypeAdmin(VersionAdmin):
    list_display = ('id', 'name', 'created_at', 'order_num')
    list_display_links = ('id', 'name')
    list_editable = ('order_num',)
    search_fields = ('id', 'name')
    date_hierarchy = 'created_at'
    actions_on_bottom = True


class ResourceAdminInline(admin.StackedInline):
    model = Resource
    extra = 0
    show_change_link = True
    classes = ('collapse',)


class ImportedResourceBaseAdmin(VersionAdmin):
    list_display = ('id', 'name', 'created_at', 'is_ignored', 'resource')
    list_display_links = ('id', 'name')
    readonly_fields = ('id', 'created_at')
    search_fields = ('id', 'name')
    date_hierarchy = 'created_at'
    actions_on_bottom = True
    actions = ('ignore', 'unignore')

    def ignore(self, request, queryset):
        queryset.ignore()
    ignore.short_description = 'Заигнорить'

    def unignore(self, request, queryset):
        queryset.unignore()
    unignore.short_description = 'Разигнорить'


@admin.register(ImportedResource)
class ImportedResourceAdmin(ImportedResourceBaseAdmin,
                            PolymorphicParentModelAdmin):
    base_model = ImportedResource
    child_models = (ImportedResourceRepo,)
    list_filter = ('is_ignored', PolymorphicChildModelFilter)


@admin.register(ImportedResourceRepo)
class ImportedResourceRepoAdmin(DjangoObjectActions,
                                ImportedResourceBaseAdmin,
                                PolymorphicChildModelAdmin):
    base_model = ImportedResourceRepo
    show_in_index = True

    list_filter = ('is_ignored',)
    inlines = (ResourceAdminInline,)

    @staticmethod
    def _redirect_to_list(params: dict) -> HttpResponseRedirect:
        filters = params.get('_changelist_filters', '')
        url = reverse('admin:main_importedresourcerepo_changelist')
        return HttpResponseRedirect(url + '?' + filters)

    def import_from_github(self, request, queryset):
        imported_resources = github.import_data()
        count = len(imported_resources)
        self.message_user(request, f'Импортировано ресурсов: {count}')
        return self._redirect_to_list(request.GET)
    import_from_github.label = 'Импортировать из GitHub'

    def create_resources(self, request, queryset):
        resources = github.create_resources()
        count = len(resources)
        self.message_user(request, f'Создано ресурсов: {count}')
        return self._redirect_to_list(request.GET)
    create_resources.label = 'Создать недостающие'

    def create_resource(self, request, obj: base_model):
        resource = github.create_resource(obj)
        if resource:
            url = reverse('admin:main_resource_change',
                          args=(resource.id,))
        else:
            url = reverse('admin:main_importedresourcerepo_change',
                          args=(obj.id,))
            self.message_user(request, 'Импортированный ресурс в игноре', 'WARNING')
        return HttpResponseRedirect(url)
    create_resource.label = 'Создать ресурс'

    changelist_actions = ('import_from_github', 'create_resources')
    change_actions = ('create_resource',)


class TagValueAdminInline(admin.TabularInline):
    model = TagValue
    extra = 1
    classes = ('collapse',)


@admin.register(Tag)
class TagAdmin(VersionAdmin):
    list_display = ('id', 'name', 'created_at', 'order_num', 'like')
    list_display_links = ('id', 'name')
    list_filter = ('like',)
    list_editable = ('order_num', 'like')
    search_fields = ('id', 'name')
    date_hierarchy = 'created_at'
    inlines = (TagValueAdminInline,)
    actions_on_bottom = True


@admin.register(TagValue)
class TagValueAdmin(AutocompleteFilterMixin, VersionAdmin):
    list_display = ('id', 'tag', 'name', 'is_default', 'created_at', 'order_num')
    list_filter = (
        'is_default',
        ('tag', AutocompleteListFilter),
    )
    list_editable = ('order_num',)
    search_fields = ('id', 'name')
    date_hierarchy = 'created_at'
    actions_on_bottom = True


@admin.register(Skill)
class SkillAdmin(MPTTModelAdmin, AutocompleteFilterMixin, VersionAdmin):
    list_display = ('id', 'name', 'parent', 'created_at',
                    'planned_progress_points', 'difficulty_points')
    list_filter = (
        ('parent', AutocompleteListFilter),
    )
    list_editable = ('planned_progress_points', 'difficulty_points')
    search_fields = ('id', 'name')
    date_hierarchy = 'created_at'
    actions_on_bottom = True


@admin.register(Task)
class TaskAdmin(MPTTModelAdmin, AutocompleteFilterMixin, VersionAdmin):
    list_display = ('id', 'name', 'created_at', 'order_num', 'like', 'skill', 'project',
                    'planned_progress_points', 'difficulty_points', 'completed')
    list_filter = (
        'completed',
        'like',
        ('parent', AutocompleteListFilter),
    )
    list_editable = ('order_num',)
    search_fields = ('id',)
    date_hierarchy = 'created_at'
    actions_on_bottom = True


@admin.register(Note)
class NoteAdmin(AutocompleteFilterMixin, VersionAdmin):
    list_display = ('id', 'created_at', 'short_content')
    list_filter = (
        ('skills', AutocompleteListFilter),
        ('resources', AutocompleteListFilter),
        ('tag_values', AutocompleteListFilter),
    )
    search_fields = ('id',)
    date_hierarchy = 'created_at'
    actions_on_bottom = True

    def short_content(self, obj):
        return obj.description[:50]
    short_content.short_description = 'Короткое содержание'
