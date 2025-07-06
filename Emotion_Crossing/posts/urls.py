from django.urls import path
from .views import PostCreateView, PostDetailView, PostLikeView, PostCheerView

urlpatterns = [
    path('posts', PostCreateView.as_view(), name='post-create'),
    path('posts/<uuid:post_id>',PostDetailView.as_view(), name='post-detail'),
    path('posts/<uuid:post_id>/like', PostLikeView.as_view(), name='post-like'),
    path('posts/<uuid:post_id>/cheer', PostCheerView.as_view(), name='post-cheer'),
]
