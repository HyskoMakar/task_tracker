import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Comment

@receiver(post_delete, sender=Comment)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.media:
        if os.path.isfile(instance.media.path):
            os.remove(instance.media.path)

@receiver(pre_save, sender=Comment)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = Comment.objects.get(pk=instance.pk).media
    except Comment.DoesNotExist:
        return False

    new_file = instance.media
    
    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)