from django.shortcuts import render
from django.db.models import OuterRef, Subquery
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .models import BoxPaf
from .models import BoxOp
from .models import Stock_consommable, StockBureau, TransfertStock
from .models import Vignettes
from .models import Bobine
from .models import Imprimante
from .models import NiveauEncre, CouleurEncre
from consommables.models import Consommable
from .serializers import boxPafSerializer
from .serializers import boxOpSerializer
from .serializers import stockSerializer
from .serializers import vignetteSerializer
from .serializers import bobineSerializer
from .serializers import boxOpSerializer
from .serializers import imprimanteSerializer
from django.utils import timezone
from datetime import timedelta
import traceback

class boxPafViewSet(viewsets.ModelViewSet):
    queryset = BoxPaf.objects.all()
    serializer_class = boxPafSerializer

    def create(self, request, *args, **kwargs):
        num = request.data.get('numero_boxPaf', '').strip()

        errors = {}

        if not num:
            errors['numero_boxPaf'] = "Le numero est obligatoire"

        if num and BoxPaf.objects.filter(numero_boxPaf__iexact=num).exists():
            errors['numero_boxPaf'] = "Ce numero du boxe paf existe déjà"

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
        boxpaf = BoxPaf.objects.create(
            numero_boxPaf=num,
        )

        return Response({
            "message": "Boxe paf crée",
            "data": boxPafSerializer(boxpaf).data
        }, status=status.HTTP_201_CREATED)
    
    #Update
    def update(self, request, *args, **kwargs):
        try:
            boxpaf = self.get_object()
        except BoxPaf.DoesNotExist:
            return Response(
                {"error": "Boxe paf introuvable"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        num = request.data.get('numero_boxPaf', '').strip()

        errors = {}

        if num and BoxPaf.objects.filter(
            numero_boxPaf__iexact=num
        ).exclude(pk=boxpaf.pk).exists():
            errors['numero_boxPaf'] = "Ce boxe paf existe déjà"

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
        if num:
            boxpaf.numero_boxPaf = num

        boxpaf.save()

        return Response({
            "message": "Boxe paf mis à jour",
            "data": boxPafSerializer(boxpaf).data
        }, status=status.HTTP_200_OK)
    
    # DELETE
    def destroy(self, request, *args, **kwargs):
        try:
            boxpaf = self.get_object()
            boxpaf.delete()
            return Response(
                {"message": "Boxe paf supprimé"},
                status=status.HTTP_200_OK
            )
        except BoxPaf.DoesNotExist:
            return Response(
                {"error": "boxe paf introuvable"},
                status=status.HTTP_404_NOT_FOUND
            )


class boxOpViewSet(viewsets.ModelViewSet):
    queryset = BoxOp.objects.all()
    serializer_class = boxOpSerializer

    def create(self, request, *args, **kwargs):
        num = request.data.get('numero_boxOp', '').strip()

        errors = {}

        if not num:
            errors['numero_boxOp'] = "Le numero est obligatoire"

        if num and BoxOp.objects.filter(numero_boxOp__iexact=num).exists():
            errors['numero_boxOp'] = "Ce numero du boxe opérateur existe déjà"

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
        boxOp = BoxOp.objects.create(
            numero_boxOp=num,
        )

        return Response({
            "message": "Boxe Opérateur crée",
            "data": boxOpSerializer(boxOp).data
        }, status=status.HTTP_201_CREATED)
    
    #Update
    def update(self, request, *args, **kwargs):
        try:
            boxOp = self.get_object()
        except BoxOp.DoesNotExist:
            return Response(
                {"error": "Boxe operateur introuvable"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        num = request.data.get('numero_boxOp', '').strip()

        errors = {}

        if num and BoxOp.objects.filter(
            numero_boxOp__iexact=num
        ).exclude(pk=boxOp.pk).exists():
            errors['numero_boxOp'] = "Ce boxe opérateur existe déjà"

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
        if num:
            boxOp.numero_boxOp = num

        boxOp.save()

        return Response({
            "message": "Boxe operateur mis à jour",
            "data": boxOpSerializer(boxOp).data
        }, status=status.HTTP_200_OK)
    
    # DELETE
    def destroy(self, request, *args, **kwargs):
        try:
            boxOp = self.get_object()
            boxOp.delete()
            return Response(
                {"message": "Boxe opérateur supprimé"},
                status=status.HTTP_200_OK
            )
        except BoxOp.DoesNotExist:
            return Response(
                {"error": "boxe opérateur introuvable"},
                status=status.HTTP_404_NOT_FOUND
            )

class stockViewSet(viewsets.ModelViewSet):
    queryset = Stock_consommable.objects.all()
    serializer_class = stockSerializer

    def create(self, request, *args, **kwargs):
        # Injecter le technicien connecté automatiquement
        user = getattr(request, 'current_user', None)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Sauvegarder avec le user
        serializer.save(user=user)

        return Response({
            "message": "Mouvement enregistré",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'], url_path='last/(?P<consommable_id>[^/.]+)')
    def last_stock(self, request, consommable_id=None):
        stock = Stock_consommable.objects.filter(
            consommable_id=consommable_id
        ).order_by('-id').first()

        if stock:
            return Response({
                "qte_restant": stock.qte_restant
            })
        return Response({
            "qte_restant": 0
        })
    

class vignetteViewSet(viewsets.ModelViewSet):
    queryset = Vignettes.objects.all()
    serializer_class = vignetteSerializer

    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)

        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

class bobineViewSet(viewsets.ModelViewSet):
    queryset = Bobine.objects.filter(
        Q(est_terminee=False) |
        Q(est_terminee=True, date_modif__date=timezone.now().date())
        ).order_by('est_terminee')
    
    serializer_class = bobineSerializer

    @action(detail=False, methods=['post'])
    def createBobine(self, request):
        bobines_data = request.data.get('bobines', [])
        # récupérer tous les box_paf concernés
        box_paf_ids = [
            b.get('box_paf') for b in bobines_data if b.get('box_paf')
        ]

        with transaction.atomic():
            #update en une seule requête
            Bobine.objects.filter(
                box_paf_id__in=box_paf_ids,
                est_terminee=False
            ).update(est_terminee=True,
                    date_modif=timezone.now()
                    )

            serializer = self.get_serializer(data=request.data.get('bobines', []), many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response(serializer.data)

class boxOpViewSet(viewsets.ModelViewSet):
    queryset = BoxOp.objects.all()
    serializer_class = boxOpSerializer

    def get_boxop():
        data = boxOpSerializer(BoxOp.objects.all(), many=True).data
        return Response(data)
    
class imprimanteViewSet(viewsets.ModelViewSet):
    queryset = Imprimante.objects.all()
    serializer_class = imprimanteSerializer

    def create(self, request, *args, **kwargs):
        print("DATA:", request.data)

        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

#apropos de l'encre
class NiveauEncreListView(APIView):
    def get(self, request):
        try:
            couleurs = CouleurEncre.objects.all()
            boxops = BoxOp.objects.all().order_by('numero_boxOp')
            
            data = []
            for couleur in couleurs:
                row = {
                    "couleur_id": couleur.id,
                    "couleur": couleur.nom,
                    "reserve": couleur.reserve,
                    "status": get_status(couleur.reserve),
                    "niveaux": {}
                }
                for box in boxops:
                    niveau = NiveauEncre.objects.filter(
                        boxOp=box,
                        couleur=couleur
                    ).first()
                    row["niveaux"][str(box.id)] = {
                        "boxop_id": box.id,
                        "numero": box.numero_boxOp,
                        "niveau": niveau.niveau if niveau else 100,
                        "niveau_id": niveau.id if niveau else None,
                    }
                data.append(row)

            # Retourner aussi la liste des boxops pour les colonnes
            boxops_list = [
                {"id": b.id, "numero": b.numero_boxOp}
                for b in boxops
            ]

            return Response({"data": data, "boxops": boxops_list})

        except Exception as e:
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)


class NiveauEncreUpdateView(APIView):
    def post(self, request, pk=None):
        try:
            boxop_id = request.data.get('boxop_id')
            couleur_id = request.data.get('couleur_id')
            niveau = request.data.get('niveau')

            print("NIVEAU RECU:", niveau, type(niveau))
            print("BOXOP ID:", boxop_id)
            print("COULEUR ID:", couleur_id)

             # S'assurer que niveau est un entier
            niveau = int(niveau)

            # Créer ou mettre à jour le niveau
            encre, created = NiveauEncre.objects.update_or_create(
                boxOp_id=boxop_id,
                couleur_id=couleur_id,
                defaults={
                    'niveau': niveau,
                    'updated_at': timezone.now()
                }
            )

            print("ENCRE SAUVEGARDÉ:", encre.id, "Créé:", created)
            return Response({"message": "Niveau mis à jour", "niveau": niveau})

        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)


class ReserveEncreUpdateView(APIView):
    def post(self, request, pk=None):
        try:
            couleur_id = request.data.get('couleur_id')
            reserve = request.data.get('reserve')

            print("RESERVE RECU:", reserve, type(reserve))
            print("COULEUR ID:", couleur_id)

            reserve = int(reserve)

            couleur = CouleurEncre.objects.get(id=couleur_id)
            couleur.reserve = reserve
            couleur.save()

            print("RESERVE SAUVEGARDÉ:", couleur.reserve)
            return Response({"message": "Réserve mise à jour", "reserve": reserve})

        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)


def get_status(reserve):
    if reserve <= 2:
        return 'épuisé'
    if reserve <= 5:
        return 'presque épuisé'
    return 'Disponible'

class HistoriqueStockView(APIView):
    def get(self, request):
        try:
            # Récupérer tous les mouvements triés du plus récent
            mouvements = Stock_consommable.objects.select_related(
                'consommable', 'user'
            ).order_by('-date_mouvement')

            data = []
            for m in mouvements:
                user_prenom = m.user.prenom if m.user else 'Inconnu'
                nom_conso = m.consommable.nom_consommable
                date = m.date_mouvement.strftime('%d %B %Y')

                # Construire le message selon entrée ou sortie
                if m.qte_entree > 0:
                    message = f"{user_prenom} a enregistré {m.qte_entree} {nom_conso} entrée"
                    type_mouvement = 'entree'
                else:
                    message = f"{user_prenom} a utilisé {m.qte_sortie} {nom_conso}"
                    type_mouvement = 'sortie'

                data.append({
                    "id": m.id,
                    "message": message,
                    "date": date,
                    "date_raw": m.date_mouvement,
                    "type": type_mouvement,
                    "user_prenom": user_prenom,
                    "consommable": nom_conso,
                    "qte_entree": m.qte_entree,
                    "qte_sortie": m.qte_sortie,
                })

            return Response(data)

        except Exception as e:
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)


class HistoriqueDeleteView(APIView):
    def delete(self, request):
        try:
            intervalle = request.data.get('intervalle')  # aujourd'hui/semaine/mois/tout
            now = timezone.now()

            if intervalle == 'aujourd_hui':
                date_limite = now.replace(hour=0, minute=0, second=0)
            elif intervalle == 'semaine':
                date_limite = now - timedelta(days=7)
            elif intervalle == 'mois':
                date_limite = now - timedelta(days=30)
            elif intervalle == 'tout':
                Stock_consommable.objects.all().delete()
                return Response({"message": "Tout l'historique supprimé"})
            else:
                return Response({"error": "Intervalle invalide"}, status=400)

            Stock_consommable.objects.filter(
                date_mouvement__gte=date_limite
            ).delete()

            return Response({"message": f"Historique '{intervalle}' supprimé"})

        except Exception as e:
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)

class StockBureauView(APIView):
    def get(self, request):
        """Récupérer le restant actuel par consommable"""
        consommable_id = request.GET.get('consommable_id')
        if not consommable_id:
            return Response({"error": "consommable_id requis"}, status=400)

        try:
            # Calculer le restant depuis le dernier mouvement
            dernier = StockBureau.objects.filter(
                consommable_id=consommable_id
            ).order_by('-date_mouvement_bureau').first()

            if not dernier:
                return Response({"qte_restant_bureau": 0, "existe": False})

            return Response({
                "qte_restant_bureau": dernier.qte_restant_bureau,
                "existe": True
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    
    def post(self, request):
        user = getattr(request, 'current_user', None)
        consommable_id = request.data.get('consommable_id')
        qte_entree = int(request.data.get('qte_entree_bureau', 0) or 0)
        qte_envoye = int(request.data.get('qte_envoye', 0) or 0)
        qte_restant_actuel = int(request.data.get('qte_restant_bureau', 0) or 0)
        site = request.data.get('site', '').strip()

        if not consommable_id:
            return Response({"error": "Consommable requis"}, status=400)

        # Il faut au moins une entrée ou un envoi
        if qte_entree == 0 and qte_envoye == 0:
            return Response({"error": "Saisir soit au moins une entrée ou un envoi"}, status=400)
        
        # Si envoi, vérifier stock suffisant (en tenant compte de l'entrée simultanée)
        # et que le site soit renseigné
        if qte_envoye > 0:
            stock_disponible = qte_restant_actuel + qte_entree
            if qte_envoye > stock_disponible:
                return Response({"error": "Stock insuffisant"}, status=400)
            if not site:
                return Response({"error": "Site doit être remplit"}, status=400)

        nouveau_restant = qte_restant_actuel + qte_entree - qte_envoye

        mouvement = StockBureau.objects.create(
            consommable_id=consommable_id,
            qte_entree_bureau=qte_entree,
            qte_envoye_bureau=qte_envoye,
            qte_restant_bureau=nouveau_restant,
            nom_site=site if qte_envoye > 0 else None,
            user=user
        )

        # NOUVEAU : si envoi -> transfert vers le tech, en attente de validation
        if qte_envoye > 0:
            TransfertStock.objects.create(
                consommable_id=consommable_id,
                quantite=qte_envoye,
                statut='en_attente',
                admin_expediteur=user,
                stock_bureau_source=mouvement
            )

        if qte_entree > 0 and qte_envoye > 0:
            message = "Entrée enregistrée. Envoi transmis au technicien pour validation."
        elif qte_entree > 0:
            message = "Entrée enregistrée"
        else:
            message = "Envoi transmis au technicien pour validation"

        return Response({
            "message": message,
            "qte_restant_bureau": nouveau_restant
        }, status=201)


class StockBureauAlerteView(APIView):
    def get(self, request):
        # Sous-requête : dernier mouvement de stock pour chaque consommable
        dernier_mouvement = StockBureau.objects.filter(
            consommable=OuterRef('pk')
        ).order_by('-date_mouvement_bureau', '-id')

        consommables = Consommable.objects.annotate(
            dernier_restant=Subquery(dernier_mouvement.values('qte_restant_bureau')[:1])
        ).filter(
            dernier_restant__isnull=False,
            dernier_restant__lte=4
        )

        data = [
            {
                "id": c.id,
                "nom_consommable": c.nom_consommable,
                "qte_restant_bureau": c.dernier_restant,
            }
            for c in consommables
        ]

        return Response(data, status=200)
    
def get_dernier_restant(model, consommable_id, champ_restant, champ_date):
    """Récupère le qte_restant du dernier mouvement pour un consommable donné."""
    dernier = model.objects.filter(
        consommable_id=consommable_id
    ).order_by(f'-{champ_date}', '-id').first()
    return getattr(dernier, champ_restant) if dernier else 0
    

class TransfertPendingListView(APIView):
    """Le technicien récupère (poll) les transferts en attente."""

    def get(self, request):
        user = getattr(request, 'current_user', None)

        if not user or user.role != 'tech':
            return Response({"error": "Accès réservé au technicien"}, status=403)

        transferts = TransfertStock.objects.filter(
            statut='en_attente'
        ).select_related('consommable', 'admin_expediteur').order_by('-date_envoi')

        data = [
            {
                "id": t.id,
                "consommable_nom": t.consommable.nom_consommable,
                "quantite": t.quantite,
                "admin_nom": f"{t.admin_expediteur.prenom} {t.admin_expediteur.nom}" if t.admin_expediteur else "Admin",
                "date_envoi": t.date_envoi,
            }
            for t in transferts
        ]

        return Response(data, status=200)


class TransfertValiderView(APIView):
    """Le technicien valide la réception -> ajoute au stock dépôt B."""

    def post(self, request, transfert_id):
        user = getattr(request, 'current_user', None)

        if not user or user.role != 'tech':
            return Response({"error": "Accès réservé au technicien"}, status=403)

        try:
            transfert = TransfertStock.objects.get(id=transfert_id, statut='en_attente')
        except TransfertStock.DoesNotExist:
            return Response({"error": "Transfert introuvable ou déjà traité"}, status=404)

        restant_b = get_dernier_restant(
            Stock_consommable, transfert.consommable_id, 'qte_restant', 'date_mouvement'
        )
        nouveau_restant_b = restant_b + transfert.quantite

        Stock_consommable.objects.create(
            consommable_id=transfert.consommable_id,
            qte_entree=transfert.quantite,
            qte_sortie=0,
            qte_restant=nouveau_restant_b,
            user=user
        )

        transfert.statut = 'valide'
        transfert.tech_receveur = user
        transfert.date_validation = timezone.now()
        transfert.save()

        return Response({
            "message": "Réception validée",
            "qte_restant": nouveau_restant_b
        }, status=200)
    

class TransfertRefuserView(APIView):
    """Le technicien refuse -> le stock retourne automatiquement au dépôt A."""

    def post(self, request, transfert_id):
        user = getattr(request, 'current_user', None)

        if not user or user.role != 'tech':
            return Response({"error": "Accès réservé au technicien"}, status=403)

        try:
            transfert = TransfertStock.objects.get(id=transfert_id, statut='en_attente')
        except TransfertStock.DoesNotExist:
            return Response({"error": "Transfert introuvable ou déjà traité"}, status=404)

        restant_a = get_dernier_restant(
            StockBureau, transfert.consommable_id, 'qte_restant_bureau', 'date_mouvement_bureau'
        )
        nouveau_restant_a = restant_a + transfert.quantite

        StockBureau.objects.create(
            consommable_id=transfert.consommable_id,
            qte_entree_bureau=transfert.quantite,
            qte_envoye_bureau=0,
            qte_restant_bureau=nouveau_restant_a,
            nom_site=None,
            user=user
        )

        transfert.statut = 'refuse'
        transfert.tech_receveur = user
        transfert.date_validation = timezone.now()
        transfert.save()

        return Response({
            "message": "Transfert refusé, stock remis dans le dépôt A",
            "qte_restant_bureau": nouveau_restant_a
        }, status=200)
# Create your views here.
