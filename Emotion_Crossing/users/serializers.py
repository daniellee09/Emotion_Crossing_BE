from rest_framework import serializers
from models import User, Character

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ('character_id', 'name', 'image_url')

class UserSerializer(serializers.ModelSerializer):
    profile_character = CharacterSerializer(read_only=True)
    profile_character_id = serializers.UUIDField(
        write_only=True,
        source='profile_character' # internal name 매핑 
    )
    
    class Meta:
        model = User
        fields = (
            'user_id',
            'name',
            'profile_character',
            'profile_character_id',
        )
        read_only_fields = ('user_id') # user_id는 수정 불가 