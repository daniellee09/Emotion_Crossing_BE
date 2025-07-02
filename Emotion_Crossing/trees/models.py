from django.db import models

# Create your models here.
import uuid

class Tree(models.Model):
    tree_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text="나무(클러스터) 고유 ID (UUID)")
    latitude = models.FloatField(verbose_name="트리의 위도")
    longitude = models.FloatField(verbose_name="트리의 경도")
    radius = models.IntegerField(default=500, verbose_name="트리 유효반경")
    
    class Meta:
        verbose_name = "Tree"
        verbose_name_plural = "Trees"

    def __str__(self):
        return f"Tree {self.tree_id} @ ({self.latitude:.4f}, {self.longitude:.4f})"