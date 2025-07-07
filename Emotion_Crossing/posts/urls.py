from django.urls import path
from .views import PostListCreateView, PostDetailView, PostLikeView, PostCheerView

urlpatterns = [
    path('posts', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<uuid:post_id>',PostDetailView.as_view(), name='post-detail'),
    path('posts/<uuid:post_id>/like', PostLikeView.as_view(), name='post-like'),
    path('posts/<uuid:post_id>/cheer', PostCheerView.as_view(), name='post-cheer'),
]
