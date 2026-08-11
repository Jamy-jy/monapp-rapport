from rest_framework import serializers
from .models import Consommable

class ConsommableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consommable
        fields = "__all__"
