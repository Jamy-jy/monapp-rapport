from rest_framework import serializers
from .models import RapportJournal

class RapportJournalSerializer(serializers.ModelSerializer):
    user_nom = serializers.SerializerMethodField()
    user_email = serializers.SerializerMethodField()
    is_read = serializers.SerializerMethodField()
    est_expediteur = serializers.SerializerMethodField()

    class Meta:
        model = RapportJournal
        fields = [
            'id', 'date_debut', 'date_fin',
            'email_destiny', 'objet', 'message',
            'fichier', 'created_at', 'user_nom', 'user_email', 'is_read', 'est_expediteur'
        ]

    def get_user_nom(self, obj):
        return f"{obj.user.prenom} {obj.user.nom}" if obj.user else ""
    
    def get_user_email(self, obj):
        return obj.user.email if obj.user else ""
    
    def get_is_read(self, obj):
        # current_user passé depuis la view via context
        user = self.context.get('user')
        if not user:
            return False
        return obj.lectures.filter(user=user).exists()

    def get_est_expediteur(self, obj):
        user = self.context.get('user')
        if not user:
            return False
        return obj.user == user