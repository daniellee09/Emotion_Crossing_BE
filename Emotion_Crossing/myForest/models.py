from django.db import models
from users.models import User
from trees.models import Tree
# Create your models here.
class myForest(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='myforest', help_text = "이 숲을 소유한 유저")
    tree_id = models.ForeignKey(Tree, on_delete=models.CASCADE, related_name='myforest', help_text = "내가 기록을 남긴 나무")
			
    class Meta:
        unique_together = (('user_id', 'tree_id'),) # 중복방지
        verbose_name = "MyForest"   

    def __str__(self):
        return f"{self.user_id.name} in Tree {self.tree_id.tree_id}"