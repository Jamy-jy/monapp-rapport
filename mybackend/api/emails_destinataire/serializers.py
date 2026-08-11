from rest_framework import serializers
from .models import Emails_destinataire

class emails_destinataireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emails_destinataire
        fields = "__all__"