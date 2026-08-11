import requests
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Vol, CategorieSejour, Mouvement_vol
from myrapport.models import RapportJournal
from .serializers import categorieSejourSerializer
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
import traceback

class categorieSejourViewset(viewsets.ModelViewSet):
    queryset = CategorieSejour.objects.all()
    serializer_class = categorieSejourSerializer

    def create(self, request, *args, **kwargs):
        libelle_jour = request.data.get('libelle', '').strip()
        note_visa = request.data.get('typeVisa', '').strip()

        errors = {}

        if not libelle_jour:
            errors['libelle'] = "Le libelle est obligatoire"
        if not note_visa:
            errors['typeVisa'] = "Ce champ est obligatoire"

        # visa unique
        if note_visa and CategorieSejour.objects.filter(typeVisa__iexact=note_visa).exists():
            errors['typeVisa'] = "Ce visa existe déjà"

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        visa = CategorieSejour.objects.create(
            libelle=libelle_jour,
            typeVisa=note_visa,
            )

        return Response({
            "message": "categorie créé",
            "data": categorieSejourSerializer(visa).data
        }, status=status.HTTP_201_CREATED)

    # UPDATE
    def update(self, request, *args, **kwargs):
        try:
            visa = self.get_object()
        except CategorieSejour.DoesNotExist:
            return Response(
                {"error": "categorie introuvable"},
                status=status.HTTP_404_NOT_FOUND
            )

        libelle_jour = request.data.get('libelle', '').strip()
        note_visa = request.data.get('typeVisa', '').strip()

        errors = {}

        # visa unique en excluant l'actuel
        if note_visa and CategorieSejour.objects.filter(
            typeVisa__iexact=note_visa
        ).exclude(pk=visa.pk).exists():
            errors['typeVisa'] = "Ce visa existe déjà"

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        if libelle_jour:
            visa.libelle = libelle_jour
        if note_visa:
            visa.typeVisa = note_visa

        visa.save()

        return Response({
            "message": "categorie mis à jour",
            "data": categorieSejourSerializer(visa).data
        }, status=status.HTTP_200_OK)

    # DELETE
    def destroy(self, request, *args, **kwargs):
        try:
            visa = self.get_object()
            visa.delete()
            return Response(
                {"message": "visa supprimé"},
                status=status.HTTP_200_OK
            )
        except visa.DoesNotExist:
            return Response(
                {"error": "categorie introuvable"},
                status=status.HTTP_404_NOT_FOUND
            )
        
class ExternalAPIVolView(APIView):
    def post(self, request):
        print("REQUEST DATA:", request.data)  # !voir ce qui arrive
        begin = request.data.get('begin')
        end = request.data.get('end')
        print("BEGIN:", begin)
        print("END:", end)

        if not begin or not end:
            return Response({"error": "Paramètres begin et end requis"}, status=400)

        # URL externe — variables dans settings.py
        external_url = f"{settings.EXTERNAL_API_BASE_URL}/tnr/replica/report-visa"

        try:
            res = requests.get(
                external_url,
                json={
                    'begin': begin,
                    'end': end
                },
                timeout=10
            )
            return Response(res.json(), status=res.status_code)

        except requests.exceptions.ConnectionError:
            return Response({"error": "Serveur externe inaccessible"}, status=503)
        except requests.exceptions.Timeout:
            return Response({"error": "Délai dépassé"}, status=504)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class MouvementVolCreateView(APIView):
    def post(self, request):
        numero_vol = request.data.get('numero_vol')
        date_arrivee_vol = request.data.get('date_arrivee_vol')
        date_fin_vol = request.data.get('date_fin_vol')
        mouvements = request.data.get('mouvements', [])

        if not numero_vol or not date_arrivee_vol:
            return Response({"error": "Numéro vol et date début requis"}, status=400)

        if not mouvements:
            return Response({"error": "Aucun mouvement à enregistrer"}, status=400)

        try:
            #Créer ou récupérer le vol
            vol, created = Vol.objects.get_or_create(
                numero_vol=numero_vol,
                defaults={
                    'date_arrivee_vol': date_arrivee_vol,
                    'date_fin_vol': date_fin_vol,
                }
            )

            if not created:
                # Mettre à jour les dates si le vol existe déjà
                vol.date_arrivee_vol = date_arrivee_vol
                vol.date_fin_vol = date_fin_vol
                vol.save()

            # Pour chaque mouvement — trouver CategorieSejour par typeVisa
            created_mouvements = []
            errors = []

            for mvt in mouvements:
                type_visa = mvt.get('type')     # ex: 'visa15'
                quantite = mvt.get('quantite')  # ex: 145

                # Chercher la catégorie correspondante
                try:
                    categorie = CategorieSejour.objects.get(typeVisa=type_visa)
                except CategorieSejour.DoesNotExist:
                    errors.append(f"Catégorie introuvable pour typeVisa: {type_visa}")
                    continue

                # Créer ou mettre à jour le mouvement
                mouvement, _ = Mouvement_vol.objects.update_or_create(
                    num_vol=vol,
                    sejour=categorie,
                    nb_par_sejour=quantite,
                    updated_at=timezone.now()
                )
                created_mouvements.append(mouvement.id)

            return Response({
                "message": "Enregistrement réussi",
                "vol_id": vol.id,
                "mouvements_created": len(created_mouvements),
                "errors": errors
            }, status=201)

        except Exception as e:
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)
        
class RecapHierView(APIView):
    def get(self, request):
        try:
            # Plage de temps hier
            now = timezone.now()
            hier_debut = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            hier_fin = (now - timedelta(days=1)).replace(hour=23, minute=59, second=59, microsecond=999999)

            # Dernier rapport tech envoyé hier
            dernier_rapport = RapportJournal.objects.filter(
                user__role='tech',
                created_at__range=(hier_debut, hier_fin)
            ).select_related('user').order_by('-created_at').first()

            tech_info = None
            if dernier_rapport and dernier_rapport.user:
                tech_info = {
                    "prenom": dernier_rapport.user.prenom,
                    "nom": dernier_rapport.user.nom,
                    "email": dernier_rapport.user.email,
                }

            # Vols enregistrés hier
            vols_hier = Vol.objects.filter(
                date_arrivee_vol__range=(hier_debut, hier_fin)
            ).order_by('date_arrivee_vol')

            nbr_vol = vols_hier.count()

            # Pour chaque vol — sum nb_par_sejour
            vols_data = []
            for vol in vols_hier:
                total_passagers = Mouvement_vol.objects.filter(
                    num_vol=vol
                ).aggregate(total=Sum('nb_par_sejour'))['total'] or 0

                vols_data.append({
                    "numero_vol": vol.numero_vol,
                    "total_passagers": total_passagers,
                    "date_arrivee": vol.date_arrivee_vol,
                })

            return Response({
                "tech": tech_info,
                "nbr_vol": nbr_vol,
                "vols": vols_data,
            })

        except Exception as e:
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)
# Create your views here.
