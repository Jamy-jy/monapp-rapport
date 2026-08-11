from rest_framework import serializers
from .models import GroupInventaire, ComposantGroup, Site

class GroupInventaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupInventaire
        fields = "__all__"

class ComposantGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComposantGroup
        fields = '__all__'

class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = "__all__"
