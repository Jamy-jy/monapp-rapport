from django.utils import timezone
from rest_framework import serializers
from .models import BoxPaf
from .models import BoxOp
from .models import Stock_consommable
from .models import Vignettes
from .models import Bobine
from .models import Imprimante

class boxPafSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoxPaf
        fields = "__all__"

class boxOpSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoxOp
        fields = "__all__"

class stockSerializer(serializers.ModelSerializer):
    user_prenom = serializers.SerializerMethodField()
    nom_consommable = serializers.SerializerMethodField()

    class Meta:
        model =  Stock_consommable
        fields = "__all__"
    
    def get_user_prenom(self, obj):
        return obj.user.prenom if obj.user else 'Inconnu'

    def get_nom_consommable(self, obj):
        return obj.consommable.nom_consommable if obj.consommable else ''

class vignetteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vignettes
        fields = "__all__"

class bobineSerializer(serializers.ModelSerializer):
    box_paf = boxPafSerializer(read_only=True)
    box_paf_id = serializers.PrimaryKeyRelatedField(
        queryset=BoxPaf.objects.all(),
        source='box_paf',
        write_only=True
    )
    
    class Meta:
        model = Bobine
        fields = "__all__"

    def validate(self, data):
        if data['debut_serie'] > data['fin_serie']:
            raise serializers.ValidationError("Invalid series range")
        return data
    
    def create(self, validated_data):
        box_paf = validated_data.get('box_paf')

        if box_paf:
            # mettre à jour les anciennes bobines non terminées
            Bobine.objects.filter(
                box_paf=box_paf,
                est_terminee=False
            ).update(
                est_terminee=True,
                date_modif=timezone.now()
                )

        return super().create(validated_data)
    
    def get_box_paf(self, obj):
        return {
            "id": obj.box_paf.id if obj.box_paf else None,
            "numero_boxPaf": obj.box_paf.numero_boxPaf if obj.box_paf else None
        }

class imprimanteSerializer(serializers.ModelSerializer):
    boxOp = serializers.PrimaryKeyRelatedField(
        queryset=BoxOp.objects.all()
    )
    class Meta:
        model = Imprimante
        fields = "__all__"

