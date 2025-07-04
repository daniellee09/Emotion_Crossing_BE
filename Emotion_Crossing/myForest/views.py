from rest_framework import viewsets
from .serializers import MyForestSerializer
from .models import myForest
from users.authentication import UserIDAuthentication

# Create your views here.
# GET 기록을 남긴 모든 나무 조회 
class MyForestViewSet(viewsets.ReadOnlyModelViewSet):
    # 내 숲 정보를 조회하는 ViewSet
    # 클라이언트가 요청 헤더에 'X-USER-ID'를 포함해서 보내야 한다.
    authentication_classes = [UserIDAuthentication]
    serializer_class = MyForestSerializer
    
    def get_queryset(self):
        # 요청 헤더의 user_id를 기반으로 해당 사용자의 숲을 반환
        return myForest.objects.filter(user=self.request.user)
        
        