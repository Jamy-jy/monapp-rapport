from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Consommable
from stock_consommables.models import Stock_consommable
from .serializers import ConsommableSerializer
from rest_framework.views import APIView
from django.db.models import Q
from django.db import models
import traceback
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from datetime import datetime, timezone as tz
from django.utils import timezone
from django.db.models import Max

class consommableViewset(viewsets.ModelViewSet):
    queryset = Consommable.objects.all()
    serializer_class = ConsommableSerializer

    def create(self, request, *args, **kwargs):
        nom = request.data.get('nom_consommable', '').strip()
        type_c = request.data.get('type_consommable', '').strip()
        mode = request.data.get('mode_consommation', '').strip()

        errors = {}

        if not nom:
            errors['nom_consommable'] = "Le nom est obligatoire"
        if not type_c:
            errors['type_consommable'] = "Le type est obligatoire"
        if not mode:
            errors['mode_consommation'] = "Le mode est obligatoire"

        # Nom unique
        if nom and Consommable.objects.filter(nom_consommable__iexact=nom).exists():
            errors['nom_consommable'] = "Ce consommable existe déjà"

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        consommable = Consommable.objects.create(
            nom_consommable=nom,
            type_consommable=type_c,
            mode_consommation=mode
        )

        return Response({
            "message": "Consommable créé",
            "data": ConsommableSerializer(consommable).data
        }, status=status.HTTP_201_CREATED)

    # UPDATE
    def update(self, request, *args, **kwargs):
        try:
            consommable = self.get_object()
        except Consommable.DoesNotExist:
            return Response(
                {"error": "Consommable introuvable"},
                status=status.HTTP_404_NOT_FOUND
            )

        nom = request.data.get('nom_consommable', '').strip()
        type_c = request.data.get('type_consommable', '').strip()
        mode = request.data.get('mode_consommation', '').strip()

        errors = {}

        # Nom unique en excluant l'actuel
        if nom and Consommable.objects.filter(
            nom_consommable__iexact=nom
        ).exclude(pk=consommable.pk).exists():
            errors['nom_consommable'] = "Ce consommable existe déjà"

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        if nom:
            consommable.nom_consommable = nom
        if type_c:
            consommable.type_consommable = type_c
        if mode:
            consommable.mode_consommation = mode

        consommable.save()

        return Response({
            "message": "Consommable mis à jour",
            "data": ConsommableSerializer(consommable).data
        }, status=status.HTTP_200_OK)

    # DELETE
    def destroy(self, request, *args, **kwargs):
        try:
            consommable = self.get_object()
            consommable.delete()
            return Response(
                {"message": "Consommable supprimé"},
                status=status.HTTP_200_OK
            )
        except Consommable.DoesNotExist:
            return Response(
                {"error": "Consommable introuvable"},
                status=status.HTTP_404_NOT_FOUND
            )
        
class DernierRestantView(APIView):
    def get(self, request):
        nom = request.GET.get('nom', '')

        if not nom:
            return Response({"error": "Paramètre nom requis"}, status=400)

        try:
            # Recherche insensible à la casse + singulier/pluriel
            stock = Stock_consommable.objects.filter(
                Q(consommable__nom_consommable__iexact=nom) |
                Q(consommable__nom_consommable__iexact=nom + 's') |
                Q(consommable__nom_consommable__iexact=nom.rstrip('s'))
            ).order_by('-date_mouvement').first()

            if not stock:
                return Response({"qte_restant": 0, "nom": nom}, status=200)

            return Response({
                "qte_restant": stock.qte_restant,
                "qte_entree": stock.qte_entree,
                "qte_sortie": stock.qte_sortie,
                "nom": stock.consommable.nom_consommable,
                "date": stock.date_mouvement,
            })

        except Exception as e:
            return Response({"error": str(e)}, status=500)

class RamPapierView(APIView):
    def get(self, request):
        try:
            stocks = Stock_consommable.objects.filter(
                Q(consommable__nom_consommable__iexact='ram') |
                Q(consommable__nom_consommable__iexact='rams') |
                Q(consommable__nom_consommable__iexact='papier') |
                Q(consommable__nom_consommable__iexact='ram papier'),
            ).order_by('date_mouvement')  # 

            if not stocks.exists():
                return Response({"pourcentage": 0, "pourcentage_total": 0})

            now = datetime.now(tz=tz.utc)

            # Première entrée — point de départ du compteur
            premiere_entree = stocks.filter(qte_entree__gt=0).first()
            if not premiere_entree:
                return Response({"pourcentage": 0, "pourcentage_total": 0})

            #  Calcul en heures pour avoir des fractions de jour
            delta = now - premiere_entree.date_mouvement
            jours_ecoules = delta.total_seconds() / 86400  # 86400 = secondes par jour

            # Total des entrées cumulées
            total_entree = stocks.aggregate(
                total=Sum('qte_entree')
            )['total'] or 0

            #  Calcul final
            # total_entree * 100 = capital de base
            # jours_ecoules * 5  = consommation depuis le début
            pourcentage_total = (total_entree * 100) - (jours_ecoules * 5)
            pourcentage_total = max(0, pourcentage_total)

            # Pour le chart — clamp 0-100
            pourcentage_affiche = min(100, pourcentage_total)

            derniere = stocks.last()

            return Response({
                "pourcentage": round(pourcentage_affiche, 2),
                "pourcentage_total": round(pourcentage_total, 2),
                "total_entree": total_entree,
                "jours_ecoules": jours_ecoules,
                "qte_restant": derniere.qte_restant if derniere else 0,
            })

        except Exception as e:
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)
        
class ConsoMensuelleView(APIView):
    def get(self, request):
        try:
            annee = request.GET.get('annee', timezone.now().year)

            # Tous les consommables — pas de filtre sur nom_consommable
            conso = Stock_consommable.objects.filter(
                date_mouvement__year=annee,
                qte_sortie__gt=0
            ).annotate(
                mois=TruncMonth('date_mouvement')
            ).values('mois').annotate(
                total_sortie=Sum('qte_sortie')
            ).order_by('mois')

            # Initialiser les 12 mois à 0
            data = [0] * 12

            for item in conso:
                mois_index = item['mois'].month - 1  # janvier = index 0
                data[mois_index] = item['total_sortie']

            return Response({
                "annee": annee,
                "data": data
            })

        except Exception as e:
            import traceback
            traceback.print_exc()  # ← affiche le vrai traceback
            print("ERREUR:", str(e))
            return Response({"error": str(e)}, status=500)
        
class NotificationView(APIView):
    def get(self, request):
        try:
            # Dernière qte_restant par consommable
            derniers_stocks = Stock_consommable.objects.values(
                'consommable__id',
                'consommable__nom_consommable'
            ).annotate(
                derniere_date=Max('date_mouvement')
            )

            notifications = []

            for stock_info in derniers_stocks:
                dernier = Stock_consommable.objects.filter(
                    consommable__id=stock_info['consommable__id'],
                    date_mouvement=stock_info['derniere_date']
                ).first()

                if not dernier:
                    continue

                qte = dernier.qte_restant
                nom = stock_info['consommable__nom_consommable']

                if qte < 3:
                    notifications.append({
                        "consommable_id": stock_info['consommable__id'],
                        "nom_consommable": nom,
                        "qte_restant": qte,
                        "type": "urgent",
                        "message": f"Épuisement de {nom}",
                        "intervalle_minutes": 30,
                    })
                elif qte < 6:
                    notifications.append({
                        "consommable_id": stock_info['consommable__id'],
                        "nom_consommable": nom,
                        "qte_restant": qte,
                        "type": "alerte",
                        "message": f"Approvisionnement requis pour {nom}",
                        "intervalle_minutes": 1440,  # 24h
                    })

            return Response(notifications)

        except Exception as e:
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)
# Create your views here.
