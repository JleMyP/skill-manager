from rest_framework.viewsets import ModelViewSet

from ..models import ImportedResource
from ..serializers import ImportedResourceSerializer

__all__ = ['ImportedResourcesViewSet']


class ImportedResourcesViewSet(ModelViewSet):
    queryset = ImportedResource.objects.all()
    serializer_class = ImportedResourceSerializer
    filterset_fields = ('is_ignored',)
