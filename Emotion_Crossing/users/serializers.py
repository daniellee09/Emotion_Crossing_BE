from rest_framework import serializers
from .models import User, Character

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ('character_id', 'name', 'image_url')

class UserSerializer(serializers.ModelSerializer):
    profile_character = CharacterSerializer(read_only=True)

    # UUIDField 가 아니라 PrimaryKeyRelatedField로 바꿔야 함. 
    # UUIDField만 쓰면 profile_character_id가 UUID를 받기는 하지만 
    # character 객체로 변환할 수 없다고 함.
    profile_character_id = serializers.PrimaryKeyRelatedField(
        queryset=Character.objects.all(),
        write_only=True,
        source='profile_character'
    ) 

    
    class Meta:
        model = User
        fields = (
            'user_id',
            'name',
            'profile_character',
            'profile_character_id',
        )
        read_only_fields = ('user_id',) # user_id는 수정 불가 