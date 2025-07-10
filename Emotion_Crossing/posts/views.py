from django.shortcuts import render, get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from users.authentication import UserIDAuthentication
from .serializers import PostSerializer
from .models import Post, PostLike, PostCheer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import F
from django.db import IntegrityError


class PostListCreateView(ListCreateAPIView):
    """
    GET  /posts/posts → 전체 게시글 조회
    POST /posts/posts → 로그인한 사용자로 새 게시글 작성
    """
    serializer_class = PostSerializer
    authentication_classes = [UserIDAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Post.objects.all()  # 사용자 관계없이 전체 조회

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

class PostDetailView(RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'post_id'
    authentication_classes = [UserIDAuthentication]
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': request})
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if post.user_id != request.user:
            return Response({"detail": "작성자만 삭제 가능"}, status=403)
        return super().destroy(request, *args, **kwargs)


class PostLikeView(APIView):
    authentication_classes = [UserIDAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, post_id=post_id)

        if post.user_id == request.user:
            return Response({"detail": "자신의 글에는 공감을 누를 수 없습니다."}, status=403)

        try:
            PostLike.objects.create(user=request.user, post=post)
            post.like_count = F('like_count') + 1
            post.save()
            post.refresh_from_db()
            return Response({"like_count": post.like_count}, status=200)
        except IntegrityError:
            return Response({"detail": "이미 공감한 글입니다."}, status=400)

class PostCheerView(APIView):
    authentication_classes = [UserIDAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, post_id=post_id)

        # ✅ 자신의 글이면 위로 금지
        if post.user_id == request.user:
            return Response({"detail": "자신의 글에는 위로를 누를 수 없습니다."}, status=403)

        # ✅ 중복 위로 방지
        try:
            PostCheer.objects.create(user=request.user, post=post)
            post.cheer_count = F('cheer_count') + 1
            post.save()
            post.refresh_from_db()
            return Response({"cheer_count": post.cheer_count}, status=200)
        except IntegrityError:
            return Response({"detail": "이미 위로한 글입니다."}, status=400)