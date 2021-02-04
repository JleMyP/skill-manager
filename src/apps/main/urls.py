from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter

from .views import ImportedResourcesViewSet, TagsViewSet


router = DefaultRouter()
router.register('imported_resources', ImportedResourcesViewSet)
router.register('tags', TagsViewSet)


urlpatterns = [
    url(r'^api/v1/', include(router.urls)),
]
