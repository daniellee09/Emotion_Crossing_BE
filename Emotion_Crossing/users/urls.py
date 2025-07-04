from django.urls import path, include
from .views import SignUpApiView, CurrentUserApiView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('signup', SignUpApiView.as_view(), name='signup'),
    path('mypage', CurrentUserApiView.as_view(), name='mypage'),
]
