from django.contrib import admin
from .models import myForest

@admin.register(myForest)
class MyForestAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'tree_id')
