from django.templatetags.static import static
from rest_framework import serializers
from .models import User, Character

class CharacterSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Character
        fields = ('character_id', 'name', 'image_url')
        
    def get_image_url(self, obj):
        # static('images/characters/xxx.png') → '/static/images/characters/xxx.png'
        rel = f'static/images/characters/{obj.image_url}'
        return self.context['request'].build_absolute_uri(static(rel))        

class UserSerializer(serializers.ModelSerializer):
    profile_character = CharacterSerializer(read_only=True)

    # profile_character_id는 UUID를 받아서 Character 객체로 변환해야 하므로,
    # UUIDField 대신 PrimaryKeyRelatedField를 사용해야 함.
    # UUIDField만 사용하면 FK 필드에 UUID 문자열이 그대로 들어가 에러 발생.
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