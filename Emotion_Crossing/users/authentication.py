from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User

# 로그인 기능 없이 들어오는 요청마다 헤더에 담긴 X-USER-ID 값을 읽어옴
# 그 UUID에 해당하는 User 객체를 찾아서 request.user로 세팅해 주는 것 
class UserIDAuthentication(BaseAuthentication):
    def authenticate(self, request):
        uid = request.headers.get("X-USER-ID") # 클라이언트가 매번 자신의 user_id를 헤더로 보내기 
        if not uid:
            return None
        try:
            user = User.objects.get(user_id=uid)
        except User.DoesNotExist:
            raise AuthenticationFailed("Invalid X-USER-ID")
        return (user, None) # View나 Permission 클래스에서 이 user를 그대로 사용해서 "현재 요청을 보낸 사용자"라고 믿음 
    # 이후 비즈니스 로직 구현 