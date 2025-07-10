from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.authentication import UserIDAuthentication
from posts.models import Post

class MyForestViewSet(ViewSet):
    authentication_classes = [UserIDAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user

        # 유저가 쓴 모든 포스트 불러오기
        user_posts = Post.objects.filter(user_id=user).select_related('tree_id')

        if not user_posts.exists():
            return Response({
                "summary": {
                    "total_post_count": 0,
                    "total_like_count": 0,
                    "total_cheer_count": 0
                },
                "trees": []
            })

        # 총합 계산
        total_post_count = user_posts.count()
        total_like_count = sum(post.like_count for post in user_posts)
        total_cheer_count = sum(post.cheer_count for post in user_posts)

        # tree_id 기준으로 묶기
        tree_map = {}
        for post in user_posts:
            tree_uuid = str(post.tree_id.tree_id)
            if tree_uuid not in tree_map:
                tree_map[tree_uuid] = {
                    "tree_id": tree_uuid,
                    "posts": []
                }
            tree_map[tree_uuid]["posts"].append(str(post.post_id))

        return Response({
            "summary": {
                "total_post_count": total_post_count,
                "total_like_count": total_like_count,
                "total_cheer_count": total_cheer_count
            },
            "trees": list(tree_map.values())
        })
