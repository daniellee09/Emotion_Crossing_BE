from django.urls import path, include
from .views import SignUpApiView, CurrentUserApiView,SignUpCharacterApiView

urlpatterns = [
    path('signup', SignUpApiView.as_view(), name='signup'),
    path('mypage', CurrentUserApiView.as_view(), name='mypage'),
    path('signup/characters', SignUpCharacterApiView.as_view(), name='signup-characters'),

]
