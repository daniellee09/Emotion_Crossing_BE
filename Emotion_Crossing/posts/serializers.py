from rest_framework import serializers
from django.templatetags.static import static
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
    user_image_url = serializers.SerializerMethodField()
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
            'post_id', 'user', 'user_name', 'user_image_url', 
            'tree', 'tree_id',
            'content', "is_private",
            'like_count', 'cheer_count', 'created_at'
        ]
        read_only_fields = ['post_id', 'user', 'user_image_url', 'user_name', 'tree', 'like_count', 'cheer_count', 'created_at']
    def get_user(self, obj):
        # 여기서 context를 넘겨야 하위 CharacterSerializer에서 image_url 생성 가능
        return UserSerializer(obj.user_id, context=self.context).data
    
    def get_user_image_url(self, obj):
        char = obj.user_id.profile_character
        if not char or not char.image_url:
            return None
        rel_path = f'images/{char.image_url}'
        return self.context['request'].build_absolute_uri(static(rel_path))