from django.urls import path, include
from .views import SignUpApiView, CurrentUserApiView

urlpatterns = [
    path('signup', SignUpApiView.as_view(), name='signup'),
    path('mypage', CurrentUserApiView.as_view(), name='mypage'),
]
