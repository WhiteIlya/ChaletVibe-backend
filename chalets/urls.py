from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChaletViewSet, UserReactionViewSet

router = DefaultRouter()  # As same as simple router but it also shows the list of paths

router.register(r'chalets', ChaletViewSet, basename='chalets')
router.register(r'reactions', UserReactionViewSet, basename='reactions')

urlpatterns = [
    path('', include(router.urls)),
]