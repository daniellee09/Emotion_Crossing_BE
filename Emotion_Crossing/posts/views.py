from django.shortcuts import render, get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from users.authentication import UserIDAuthentication
from .serializers import PostSerializer
from .models import Post
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import F


class PostListCreateView(ListCreateAPIView):
    """
    GET  /posts/ → 로그인한 사용자가 쓴 전체 포스트 조회
    POST /posts/ → 새 포스트 생성
    """
    serializer_class = PostSerializer
    authentication_classes = [UserIDAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # 로그인한 사용자(request.user) 포스트만 리턴
        return Post.objects.filter(user_id=self.request.user)

    def perform_create(self, serializer):
        # 저장할 때 user_id 필드에도 현재 사용자 지정
        serializer.save(user_id=self.request.user)

class PostDetailView(RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'post_id' # post/<uuid:post_id> 의 id와 내부적으로 맵핑
    authentication_classes = [UserIDAuthentication]
    permission_classes = [IsAuthenticated]

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