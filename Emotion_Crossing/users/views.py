from django.shortcuts import render, get_object_or_404
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from .authentication import UserIDAuthentication
from .serializers import UserSerializer, CharacterSerializer
from .models import User, Character
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


# Create your views here.
class SignUpCharacterApiView(APIView):
    authentication_classes = [UserIDAuthentication]
    permission_classes = [AllowAny]
    
    def get(self, request):
            """GET /users/signup/characters - 캐릭터 전체 목록 반환"""
            characters = Character.objects.all()
            serializer = CharacterSerializer(
                characters,
                many=True,
                context={'request': request}
            )
            return Response(serializer.data)
                            
    def patch(self, request):
        """PATCH /users/signup/characters - 사용자의 캐릭터 선택"""
        user = request.user
        serializer = UserSerializer(
            user,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        selected_character = user.profile_character  # FK로 연결된 Character 객체
        return Response({
            "message": "캐릭터가 선택되었습니다.",
            "image_url": selected_character.image_url
        }, status=status.HTTP_200_OK)

# POST /signup
class SignUpApiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
# GET /users : 내 프로필 조회
# PATCH /users : 프로필 이미지 또는 닉네임 수정 
# DELETE /users : 회원 탈퇴 
class CurrentUserApiView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [UserIDAuthentication]
    permission_classes = [AllowAny] # 인증 자체는 헤더만 보고 처리 
    serializer_class = UserSerializer
    
    # X-USER-ID 헤더로부터 현재 요청을 보낸 사용자의 UUID를 읽고,
    # 그 UUID에 해당하는 User 인스턴스를 get_object_or_404() 로 조회한 뒤
    # 반환(return)
    def get_object(self):
        # 이 뷰가 어떤 객체를 조회, 수정, 삭제 대상으로 삼을지를 결정하는 역할
        uid = self.request.headers.get("X-USER-ID")
        return get_object_or_404(User, user_id=uid) # 지금 헤더를 통해 식별된 나의 User 객체 
