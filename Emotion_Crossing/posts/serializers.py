from rest_framework import serializers
from .models import Post
from users.models import User
from trees.models import Tree
from users.serializers import UserSerializer

class TreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tree
        fields = '__all__'

## 수정사항
## 클라이언트가 넘긴 PK(UUID)를 받아서 그에 대응하는 Tree 인스턴스를 찾아 모델의 FK 필드에 넣어 주는 PrimaryKeyRelatedField를 사용해야 오류가 안 남
class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) ## source='user_id' 지정 시 불필요한 중복 지정 오류로 에러 발생해서 제거함 
    user_name = serializers.CharField(source='user_id.name', read_only=True) # 작성자 이름만 따로 표시 
    
    tree = TreeSerializer(read_only=True) ## 여기도 source='tree_id' 제거함 
    tree_id = serializers.PrimaryKeyRelatedField(
        queryset = Tree.objects.all(),
        write_only=True,
        help_text="나무 UUID"
    )
    
    class Meta:
        model = Post
        fields = [
            'post_id', 'user', 'user_name', 'tree', 'tree_id',
            'content', "is_private",
            'like_count', 'cheer_count', 'created_at'
        ]
        read_only_fields = ['post_id', 'user', 'user_name', 'tree', 'like_count', 'cheer_count', 'created_at']