from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Tree
from posts.serializers import TreeSerializer
from rest_framework.permissions import AllowAny

class TreeListView(ListAPIView):
    queryset = Tree.objects.all()
    serializer_class = TreeSerializer
    permission_classes = [AllowAny]
