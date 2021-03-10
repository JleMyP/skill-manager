from django.db.models import F
from django.db.models.functions import Lower
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ..models import ImportedResource
from ..serializers import ImportedResourcePolySerializer

__all__ = ['ImportedResourcesViewSet']


class ImportedResourcesViewSet(ModelViewSet):
    model = ImportedResource
    queryset = ImportedResource.objects.all()
    serializer_class = ImportedResourcePolySerializer
    filterset_fields = ('is_ignored',)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.action == 'list':
            return (self.model.objects.non_polymorphic()
                                      .annotate(ptype=F('polymorphic_ctype__model'),
                                                lname=Lower('name'))
                                      .order_by('lname'))
        return super().get_queryset()
