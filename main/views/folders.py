from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_serializer_extensions.views import SerializerExtensionsAPIViewMixin

from ..models import Folder

__all__ = ['FoldersViewSet']


class FoldersViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     SerializerExtensionsAPIViewMixin,
                     viewsets.GenericViewSet):
    queryset = Folder.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ('parent', 'like')
    search_fields = ('name',)
    ordering_fields = ('order_num', 'name', 'created_at')
