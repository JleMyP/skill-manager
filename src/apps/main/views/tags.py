from rest_framework.viewsets import ModelViewSet

from ..models import Tag
from ..serializers import TagSerializer

__all__ = ['TagsViewSet']


class TagsViewSet(ModelViewSet):
    model = Tag
    queryset = model.objects.all()
    serializer_class = TagSerializer
    filterset_fields = ('like',)
