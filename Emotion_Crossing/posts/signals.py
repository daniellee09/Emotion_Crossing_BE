from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from myForest.models import myForest

@receiver(post_save, sender=Post)
def create_myforest_on_post(sender, instance, created, **kwargs):
    if created:
        user = instance.user_id
        tree = instance.tree_id
        myForest.objects.get_or_create(user_id=user, tree_id=tree)
