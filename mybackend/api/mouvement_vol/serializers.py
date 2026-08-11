from rest_framework import serializers
from .models import CategorieSejour, Mouvement_vol

class categorieSejourSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategorieSejour
        fields = "__all__"

class MouvementVolCreateSerializer(serializers.Serializer):
    numero_vol = serializers.CharField()
    date_arrivee_vol = serializers.DateTimeField()
    date_fin_vol = serializers.DateTimeField()
    mouvements = serializers.ListField(
        child=serializers.DictField()
    )