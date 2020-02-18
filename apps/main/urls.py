from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter

from .views import FoldersViewSet

router = DefaultRouter()
router.register('folders', FoldersViewSet)

urlpatterns = [
    url(r'^api/v1/', include(router.urls)),
]
