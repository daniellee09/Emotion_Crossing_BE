from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MyForestViewSet

router = DefaultRouter()
router.register('', MyForestViewSet, basename='myforest') 

urlpatterns = [
    path('', include(router.urls)),
]
