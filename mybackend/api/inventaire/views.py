from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import GroupInventaire, ComposantGroup, Site
from .serializers import GroupInventaireSerializer
from .serializers import ComposantGroupSerializer
from .serializers import SiteSerializer
from django.db.models import Max, OuterRef, Subquery, F
from django.utils import timezone
from datetime import timedelta
from rest_framework.decorators import api_view
from django.db import transaction
from django.utils.dateparse import parse_datetime

class GroupInventaireViewset(viewsets.ModelViewSet):
    queryset = GroupInventaire.objects.all().order_by("-group_created_at")
    serializer_class = GroupInventaireSerializer

    def create(self, request, *args, **kwargs):
        user = getattr(request, 'current_user', None)
        nom = request.data.get("nom_group", "").strip()

        if not nom:
            return Response(
                {"error": "Le nom du groupe est obligatoire."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if GroupInventaire.objects.filter(nom_group__iexact=nom).exists():
            return Response(
                {"error": "Ce groupe existe déjà."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(user=user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        group = self.get_object()
        nom = request.data.get("nom_group", "").strip()

        if not nom:
            return Response(
                {"error": "Le nom du groupe est obligatoire."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if GroupInventaire.objects.exclude(pk=group.pk).filter(
            nom_group__iexact=nom
        ).exists():
            return Response(
                {"error": "Un groupe avec ce nom existe déjà."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        group = self.get_object()
        group.delete()

        return Response(
            {"message": "Groupe supprimé avec succès."},
            status=status.HTTP_200_OK
        )

    # ACCESS STATUT — dévérouiller/vérouiller groupe
    @action(detail=True, methods=['patch'], url_path='access-statut')
    def access_statut(self, request, pk=None):
        try:
            groupe = self.get_object()
        except GroupInventaire.DoesNotExist:
            return Response(
                {"error": "Utilisateur introuvable"},
                status=status.HTTP_404_NOT_FOUND
            )

        groupe.access_group = not groupe.access_group  # bascule true/false
        groupe.save()

        acces = "Déverouller" if groupe.access_group else "Vérouiller"

        return Response({
            "message": f"groupe {acces}",
            "accès": groupe.access_group,
            "data": GroupInventaireSerializer(groupe).data
        }, status=status.HTTP_200_OK)
    
class ComposantGroupViewSet(viewsets.ModelViewSet):
    serializer_class = ComposantGroupSerializer

    def get_queryset(self):
        queryset = ComposantGroup.objects.all().order_by('-composant_created_at')

        group_id = self.request.query_params.get('group')
        if group_id:
            queryset = queryset.filter(group_id=group_id)

        # Ne montrer que les matériels pas encore validés
        pending_only = self.request.query_params.get('pending')
        if pending_only == 'true':
            queryset = queryset.filter(Etat_materiel__isnull=True)


        # Historique : uniquement les matériels déjà testés (Oui/Non)
        historique_only = self.request.query_params.get('historique')
        if historique_only == 'true':
            queryset = queryset.filter(Etat_materiel__isnull=False)

            # Déduplication : si plusieurs lignes partagent exactement
            # nom_materiel + Etat_materiel + numero_serie + composant_created_at,
            # on ne garde que celle avec l'id le plus élevé (la dernière insérée).
            latest_ids_subquery = (
                ComposantGroup.objects.filter(
                    nom_materiel=OuterRef('nom_materiel'),
                    Etat_materiel=OuterRef('Etat_materiel'),
                    numero_serie=OuterRef('numero_serie'),
                )
                .order_by('-id')
                .values('id')[:1]
            )

            queryset = queryset.annotate(
                latest_duplicate_id=Subquery(latest_ids_subquery)
            ).filter(id=F('latest_duplicate_id'))

        date_debut = self.request.query_params.get('date_debut')
        date_fin = self.request.query_params.get('date_fin')

        if date_debut:
            parsed = parse_datetime(date_debut)
            if parsed:
                queryset = queryset.filter(composant_created_at__gte=parsed)

        if date_fin:
            parsed = parse_datetime(date_fin)
            if parsed:
                queryset = queryset.filter(composant_created_at__lte=parsed)

        return queryset


def get_latest_check_per_materiel():
    """
    Retourne, pour chaque matériel physique (group + numero_serie),
    la ligne de vérification la plus récente où Etat_materiel n'est pas null.
    """

    validated = ComposantGroup.objects.filter(Etat_materiel__isnull=False)

    latest_ids_subquery = (
        validated.filter(lineage_id=OuterRef('lineage_id'))
        .order_by('-composant_created_at')
        .values('id')[:1]
    )

    latest_per_key = (
        validated
        .values('lineage_id')
        .annotate(latest_id=Subquery(latest_ids_subquery))
        .values_list('latest_id', flat=True)
        .distinct()
    )

    return ComposantGroup.objects.filter(id__in=list(latest_per_key))

@api_view(['GET'])
def alertes_materiel(request):
    latest_rows = get_latest_check_per_materiel()
    alertes = latest_rows.filter(
        Etat_materiel=False,
        date_remplacement__isnull=True,
        ).select_related('group')

    data = [
        {
            'id': c.id,
            'group_id': c.group_id,
            'nom_group': c.group.nom_group,
            'nom_materiel': c.nom_materiel,
            'numero_serie': c.numero_serie,
            'date_constat': c.composant_created_at,
        }
        for c in alertes
    ]
    return Response(data)


CYCLE_JOURS = 30
TOLERANCE_JOURS = 3

@api_view(['GET'])
def materiels_a_verifier(request):
    today = timezone.now()
    latest_rows = get_latest_check_per_materiel().select_related('group')
    result = []
    for c in latest_rows:
        if c.Etat_materiel is None:
            # Nouveau matériel jamais testé (première mise en service OU remplacement en attente de test)
            result.append({
                'id': c.id,
                'group_id': c.group_id,
                'nom_group': c.group.nom_group,
                'nom_materiel': c.nom_materiel,
                'numero_serie': c.numero_serie,
                'derniere_verification': None,
                'prochaine_echeance': None,
                'statut': 'jamais_verifie',
            })
        else:
            prochaine_echeance = c.composant_created_at + timedelta(days=CYCLE_JOURS)
            seuil_alerte = prochaine_echeance - timedelta(days=TOLERANCE_JOURS)

            if today >= seuil_alerte:
                statut = 'en_retard' if today > prochaine_echeance + timedelta(days=TOLERANCE_JOURS) else 'a_verifier'
                result.append({
                    'id': c.id,
                    'group_id': c.group_id,
                    'nom_group': c.group.nom_group,
                    'nom_materiel': c.nom_materiel,
                    'numero_serie': c.numero_serie,
                    'derniere_verification': c.composant_created_at,
                    'prochaine_echeance': prochaine_echeance,
                    'statut': statut,
                })

    return Response(result)

@api_view(['POST'])
@transaction.atomic
def remplacer_materiel(request, ancien_id):
    try:
        ancien = ComposantGroup.objects.get(id=ancien_id)
    except ComposantGroup.DoesNotExist:
        return Response({'error': 'Matériel introuvable'}, status=404)

    if ancien.Etat_materiel is not False:
        return Response(
            {'error': "Seul un matériel non fonctionnel peut être remplacé."},
            status=400
        )

    data = request.data
    date_remplacement = data.get('date_remplacement') or timezone.now()

    nouveau = ComposantGroup.objects.create(
        group=ancien.group,
        nom_materiel=data.get('nom_materiel', ancien.nom_materiel),
        marque_materiel=data.get('marque_materiel', ancien.marque_materiel),
        numero_serie=data.get('numero_serie'),
        configuration=data.get('configuration', ancien.configuration),
        Etat_materiel=None,             # nouveau matériel : à tester
        test_fonctionnalite=None,
        lineage_id=ancien.lineage_id,   # <-- même fil de traçabilité
        remplace=ancien,
        composant_created_at=date_remplacement,
    )

    # Marque l'ancien comme remplacé (audit)
    ancien.date_remplacement = date_remplacement
    ancien.save(update_fields=['date_remplacement'])

     # --- Propagation déclenchée UNIQUEMENT à la confirmation du remplacement ---
    # On marque tout autre matériel partageant le même numéro de série que l'ANCIEN
    # (celui qui vient d'être confirmé comme non fonctionnel) comme non fonctionnel aussi.
    ComposantGroup.objects.filter(
        numero_serie=ancien.numero_serie
    ).exclude(
        id=ancien.id
    ).update(
        Etat_materiel=False,
        date_remplacement=timezone.now()
        )

    serializer = ComposantGroupSerializer(nouveau)
    return Response(serializer.data, status=201)

class SiteViewset(viewsets.ModelViewSet):
    queryset = Site.objects.all().order_by("-site_created_at")
    serializer_class = SiteSerializer
# Create your views here.
