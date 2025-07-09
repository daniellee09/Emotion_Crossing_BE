# myforest/views.py
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
        tree_ids = (
            Post.objects.filter(user_id=user)
            .values_list('tree_id', flat=True)
        )

        unique_tree_ids = list(set(tree_ids))
        if not unique_tree_ids:
            return Response({"message": "글을 작성한 나무가 없습니다", "tree_id": []})

        return Response({"tree_id": unique_tree_ids})
