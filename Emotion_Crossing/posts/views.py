from django.shortcuts import render, get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from users.authentication import UserIDAuthentication
from .serializers import PostSerializer
from .models import Post
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import F


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


# 공감하기와 위로하기 기능
class PostLikeView(APIView):
    authentication_classes = [UserIDAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, post_id=post_id)
        post.like_count = F('like_count') + 1  # F()표현식을 통한 원자적 증가. 이 방법으로 여러사용자가 클릭하는 경우를 대비할 수 있음
        post.save()
        post.refresh_from_db()  # DB에서 실제 값 다시 가져오기
        return Response({"like_count": post.like_count}, status=status.HTTP_200_OK)

class PostCheerView(APIView):
    authentication_classes = [UserIDAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, post_id=post_id)
        post.cheer_count = F('cheer_count') + 1
        post.save()
        post.refresh_from_db()
        return Response({"cheer_count": post.cheer_count}, status=status.HTTP_200_OK)