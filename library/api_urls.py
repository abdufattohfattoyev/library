from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import FanViewSet, BolimViewSet, JurnalViewSet

# Router yaratish
router = DefaultRouter()
router.register(r'fanlar', FanViewSet, basename='fan')
router.register(r'bolimlar', BolimViewSet, basename='bolim')
router.register(r'jurnallar', JurnalViewSet, basename='jurnal')

# URL patterns
urlpatterns = [
    path('', include(router.urls)),
]