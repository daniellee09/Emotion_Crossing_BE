from django.db import models

# Create your models here.
import uuid
from users.models import User
from trees.models import Tree

class Post(models.Model):
    post_id = models.UUIDField(primary_key = True, default=uuid.uuid4, editable=False, help_text="메시지 고유 ID (UUID)")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', help_text="작성자 (User FK)")
    tree_id = models.ForeignKey(Tree, on_delete=models.CASCADE, related_name='posts', help_text="소속 나무 (Tree FK)")
    content = models.TextField(max_length=100, verbose_name="기록 내용", help_text="메시지 내용 (최대 100자)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="기록 생성시간", help_text="작성 시각 자동 기록")
    like_count = models.IntegerField(default=0, verbose_name="공감 개수", help_text="👍 공감 수")
    cheer_count = models.IntegerField(default=0, verbose_name="위로 개수", help_text="💙 위로 수")
    post_latitude = models.FloatField(verbose_name="기록의 위도", help_text="정확한 메시지 위도")
    post_longitude = models.FloatField(verbose_name="기록의 경도", help_text="정확한 메시지 경도")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return f"{self.user.name} @ {self.created_at:%Y-%m-%d %H:%M}"