from django.urls import path
from .views import TreeListView

urlpatterns = [
    path('', TreeListView.as_view(), name='tree-list'),  # GET /trees/ → 전체 트리 목록 조회
]