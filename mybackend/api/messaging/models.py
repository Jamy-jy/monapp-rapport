from django.db import models
from django.conf import settings
from django.utils import timezone
from users.models import User

class ConversationType(models.TextChoices):
    SHARED_ADMIN = 'shared_admin', 'Espace commun admins'
    PRIVATE = 'private', 'Privé admin-tech'
    GROUP = 'group', 'Groupe'

class Conversation(models.Model):
    name = models.CharField(max_length=100, blank=True)
    type = models.CharField(max_length=20, choices=ConversationType.choices)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, 
        related_name='created_conversations'
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        db_table = "Conversation"

    def __str__(self):
        return self.name or f"{self.type} #{self.id}"

class ConversationMember(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
        )
    joined_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('conversation', 'user')
        db_table = "ConversationMember"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
        )
    content = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['sent_at']
        db_table = "Message"


# Create your models here.
