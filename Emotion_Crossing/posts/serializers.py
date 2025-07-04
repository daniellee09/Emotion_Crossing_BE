from rest_framework import serializers
from .models import Post
from trees.models import Tree
from users.serializers import UserSerializer

class TreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tree
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='user_id', read_only=True)
    user_id = serializers.UUIDField( #사용자의 UUID를 받는 필드
        write_only=True,
        source='user_id', # 이부분으로 사용자가 보낸 UUID와 post모델의 user_id가 내부적으로 맵핑됨
        help_text="작성자 UUID"
    )
    tree = TreeSerializer(source='tree_id', read_only=True)
    tree_id = serializers.UUIDField(
        write_only=True,
        source='tree_id',
        help_text="나무 UUID"
    )
    
    class Meta:
        model = Post
        fields = '__all__'