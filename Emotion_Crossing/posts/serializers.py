from rest_framework import serializers
from .models import Post, Tree
from .serializers import UserSerializer

class TreeSerializer(serializers.ModelSerializer):
    class Meata:
        model = Tree
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='user_id', read_only=True)
    user_id = serializers.UUIDField(
        write_only=True,
        source='user_id',
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