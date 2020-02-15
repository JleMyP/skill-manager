from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_serializer_extensions.views import SerializerExtensionsAPIViewMixin
from reversion.views import RevisionMixin

from ..models import Folder
from ..serializers.folder import FolderSerializer

__all__ = ['FoldersViewSet']


class FoldersViewSet(RevisionMixin,
                     SerializerExtensionsAPIViewMixin,
                     viewsets.ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ('parent', 'like')
    search_fields = ('name',)
    ordering_fields = ('order_num', 'name', 'created_at')
