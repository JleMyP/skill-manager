from django.db.models import F
from rest_framework.viewsets import ModelViewSet

from ..models import ImportedResource
from ..serializers import ImportedResourcePolySerializer

__all__ = ['ImportedResourcesViewSet']


class ImportedResourcesViewSet(ModelViewSet):
    model = ImportedResource
    queryset = ImportedResource.objects.all()
    serializer_class = ImportedResourcePolySerializer
    filterset_fields = ('is_ignored',)

    def get_queryset(self):
        if self.action == 'list':
            return (self.model.objects.non_polymorphic()
                                      .order_by('name')
                                      .annotate(ptype=F('polymorphic_ctype__model')))
        return super().get_queryset()
