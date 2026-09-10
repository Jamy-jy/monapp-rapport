from rest_framework import serializers
from .models import IncidentSurvenu
from users.models import User  

class IncidentSurvenuSerializers(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = IncidentSurvenu
        fields = '__all__' 

    def get_user(self, obj):
        if obj.user:
            return f"{obj.user.nom} {obj.user.prenom}"
        return None