from django.core.management.base import BaseCommand
from django.db import transaction
from users.models import User
from messaging.models import Conversation, ConversationMember, Message, ConversationType


class Command(BaseCommand):
    help = "Fusionne les conversations PRIVATE dupliquées (une par admin) en une seule conversation partagée."

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run', action='store_true',
            help="Simule la fusion sans rien modifier en base."
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        techs   = User.objects.filter(role='tech')
        admins  = list(User.objects.filter(role='admin'))

        with transaction.atomic():
            for tech in techs:
                convs = list(
                    Conversation.objects.filter(
                        type=ConversationType.PRIVATE,
                        members__user_id=tech.id
                    ).distinct().order_by('created_at')
                )

                if len(convs) <= 1:
                    continue  # rien à fusionner

                canonical  = convs[0]   # la plus ancienne = référence
                duplicates = convs[1:]

                self.stdout.write(
                    f"Tech {tech.id} ({tech.prenom} {tech.nom}) : "
                    f"{len(convs)} conversations -> fusion vers #{canonical.id}"
                )

                if dry_run:
                    continue  # on affiche seulement, on ne touche à rien

                for dup in duplicates:
                    # Déplace les messages du doublon vers la conversation canonique
                    Message.objects.filter(conversation=dup).update(conversation=canonical)
                    dup.delete()  # supprime la conv vide + ses ConversationMember (cascade)

                # S'assure que TOUS les admins actuels sont membres de la conversation canonique
                existing_ids = set(
                    ConversationMember.objects.filter(conversation=canonical)
                    .values_list('user_id', flat=True)
                )
                missing = [a for a in admins if a.id not in existing_ids]
                ConversationMember.objects.bulk_create(
                    [ConversationMember(conversation=canonical, user=a) for a in missing]
                )

            if dry_run:
                transaction.set_rollback(True)  # annule tout, même si dry_run n'a rien modifié

        if dry_run:
            self.stdout.write(self.style.WARNING("Dry-run terminé — aucune donnée modifiée."))
        else:
            self.stdout.write(self.style.SUCCESS("Fusion terminée."))