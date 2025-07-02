from django.db import models
import uuid;

# Create your models here.

class Character(models.Model):
    character_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name         = models.CharField(max_length=20)
    image_url    = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class User(models.Model):
    user_id = models.UUIDField(primary_key = True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20)
    profile_character = models.ForeignKey('Character', null=False, blank=False, on_delete=models.PROTECT)
    
    def __str__(self):
        return f"{self.name} ({self.user_id})"