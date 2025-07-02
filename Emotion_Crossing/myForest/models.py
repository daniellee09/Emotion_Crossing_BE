from django.db import models
from users.models import User
from trees.models import Tree
# Create your models here.
class myForest(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='myforest', help_text = "이 숲을 소유한 유저")
    tree_id = models.ForeignKey(Tree, on_delete=models.CASCADE, related_name='myforest', help_text = "내가 기록을 남긴 나무")
    post_count = models.IntegerField(default=0, verbose_name="기록 개수")
    first_post_at = models.DateTimeField(verbose_name="처음 글을 남긴 시각", help_text = "해당 나무에 처음 글을 남긴 시각")
    last_post_at = models.DateTimeField(verbose_name="마지막 글을 남긴 시각", help_text = "해당 나무에 마지막으로 글을 남긴 시각")
			
    class Meta:
        unique_together = (('user_id', 'tree_id'),) # 중복방지
        verbose_name = "MyForest"
        verbose_name_plural = "MyForests"

    def __str__(self):
        return f"{self.user.name} in Tree {self.tree.tree_id}"