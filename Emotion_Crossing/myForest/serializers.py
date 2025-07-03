from rest_framework import serializers
from .models import myForest
from .serializers import TreeSerializer

class MyForestSerializer(serializers.ModelSerializer):
    # 읽을 때만, MyForest.tree(FK)와 연결된 Tree 객체를 중첩해서 보여줌 
    tree = TreeSerializer(read_only=True)

    class Meta:
        model  = myForest
        # 오직 tree 정보만 노출
        fields = ('tree',)