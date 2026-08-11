from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User
from .models import Conversation, ConversationMember, ConversationType


@receiver(post_save, sender=User)
def auto_join_admin_to_existing_conversations(sender, instance, created, **kwargs):
    """
    FIX : à la création d'un nouvel admin, on l'ajoute automatiquement
    à toutes les conversations PRIVATE, GROUP et SHARED_ADMIN déjà
    existantes, pour que l'espace admin reste bien partagé entre tous.
    """
    if not created or instance.role != 'admin':
        return

    convs = Conversation.objects.filter(
        type__in=[ConversationType.PRIVATE, ConversationType.GROUP, ConversationType.SHARED_ADMIN]
    ).exclude(members__user_id=instance.id)  # évite les doublons si déjà membre

    ConversationMember.objects.bulk_create(
        [ConversationMember(conversation=conv, user=instance) for conv in convs],
        ignore_conflicts=True  # sécurité contre unique_together en cas de course
    )