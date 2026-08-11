import os
import traceback
from django.core.mail import EmailMessage
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import RapportJournal, RapportJournalLu, TextModel
from stock_consommables.models import Stock_consommable
from users.models import User
from rest_framework import status

# Create your views here

from rest_framework.decorators import api_view
from .serializers import RapportJournalSerializer

@api_view(["GET"])
def hello(request):
    return Response({"message": "Django backend OK"})

class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')

        if not file:
            return Response({"error": "No file"}, status=400)

        file_path = os.path.join(settings.MEDIA_ROOT, file.name)

        # Sauvegarde simple
        with open(file_path, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        file_url = request.build_absolute_uri(settings.MEDIA_URL + file.name)

        return Response({"message": "Uploaded", "file_url": file_url}, status=201)
    

class FileDeleteView(APIView):
    def post(self, request, *args, **kwargs):
        file_url = request.data.get('file_url')

        if not file_url:
            return Response({"error": "No file_url"}, status=400)

        # extraire le nom du fichier
        file_name = file_url.split('/media/')[-1]
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)

        if os.path.exists(file_path):
            os.remove(file_path)
            return Response({"message": "File deleted"}, status=200)
        else:
            return Response({"error": "File not found"}, status=404)
        
class SendEmailView(APIView):
    def post(self, request):
        destinataires = request.data.getlist('destinataire[]')
        cc = request.data.get('cc','')
        cci = request.data.get('cci','')
        objet = request.data.get('objet','')
        message = request.data.get('message','')
        files = request.FILES.getlist('files')
        date_debut = request.data.get('date_debut', '')
        date_fin = request.data.get('date_fin', '')

        """ expediteur = utilisateur connécté """

        user = getattr(request, 'current_user', None)
        reply_to = [user.email] if user else []

        if user:
            expediteur = f"{user.prenom} {user.nom} <{settings.DEFAULT_FROM_EMAIL}>"

        else:
            expediteur = settings.DEFAULT_FROM_EMAIL

        if not destinataires:
            return Response({"error": "No recipients"}, status=400)

        email = EmailMessage(
            subject=objet,
            body=message,
            from_email=expediteur,
            to=destinataires,
            cc=[cc] if cc else [],
            bcc=[cci] if cci else [],
            reply_to=reply_to,
        )

        print("EMAIL_HOST:", settings.EMAIL_HOST)

        # Attacher les fichiers et garder le premier pour RapportJournal
        saved_file = None
            
        for f in files:
            content = f.read()
            email.attach(f.name, f.read(), f.content_type)
            if saved_file is None:
                saved_file = f  # garder référence du premier fichier

        try:
            email.send()
        except Exception as e:
            traceback.print_exc() 
            return Response({"error": str(e)}, status=500)
 
        # Vérification de l'user
        #admin
        if user and user.role == 'admin':
            #date optionnelles
            date_debut = date_debut or None
            date_fin = date_fin or None
        #tech
        else: 
            #date obligatoire
            if not date_debut or not date_fin:
                print("Date manquantes - manquante email non envoyé")
                return Response({"message":"Email envoyé"})

        # Enregistrement RapportJournal après envoi réussi
        try:
            # Récupérer l'objet Emails_destinataire correspondant

            print("DATE DEBUT:", date_debut)
            print("DATE FIN:", date_fin)
            print("USER:", user)
            print("DESTINATAIRES:", destinataires)

            rapport = RapportJournal(
                date_debut=date_debut,
                date_fin=date_fin,
                email_destiny=', '.join(destinataires),
                cc=cc,
                cci=cci,
                user=user,
                objet=objet,
                message=message,
            )

            # Rattacher le fichier s'il existe
            if saved_file:
                saved_file.seek(0)  # remettre le curseur au début
                rapport.fichier.save(saved_file.name, saved_file, save=False)

            rapport.save()
            print(" RapportJournal enregistré")

        except Exception as e:
            # Ne pas bloquer l'envoi si l'enregistrement échoue
            traceback.print_exc()
            print("erreur enregistrement :", e)
        return Response({"message": "Email envoyé"})
    
class RapportJournalListView(APIView):
    def get(self, request):
        user = getattr(request, 'current_user', None)
        
        if not user:
            return Response({"error": "Non authentifié"}, status=401)

        # Chaque utilisateur voit uniquement ses propres rapports
        rapports = RapportJournal.objects.filter(
            user=user
        ).order_by('-created_at')

        serializer = RapportJournalSerializer(rapports, many=True)
        return Response(serializer.data)


class RapportJournalDetailView(APIView):
    def get(self, request, pk):
        user = getattr(request, 'current_user', None)
        
        try:
            rapport = RapportJournal.objects.get(pk=pk)
        except RapportJournal.DoesNotExist:
            return Response({"error": "Rapport introuvable"}, status=404)

        # Vérifier que l'user est soit l'expéditeur soit dans les destinataires
        est_expediteur = rapport.user == user
        est_destinataire = user.email in rapport.email_destiny

        print(est_expediteur)
        if not est_expediteur and not est_destinataire:
            return Response({"error": "Accès refusé"}, status=403)
        
        # Marquer comme lu si destinataire
        if est_destinataire:
            RapportJournalLu.objects.get_or_create(rapport=rapport, user=user)

        print("DETAIL VIEW USER:", user)
        print("DETAIL VIEW EST EXPEDITEUR:", rapport.user == user)

        serializer = RapportJournalSerializer(
            rapport,
            context={'user': user}  
        )

        print("SERIALIZER DATA:", serializer.data.get('est_expediteur'))
        
        return Response(serializer.data)
    
class RapportJournalRecuListView(APIView):
    def get(self, request):
        user = getattr(request, 'current_user', None)

        if not user:
            return Response({"error": "Non authentifié"}, status=401)

        # Exclure les rapports marqués is_delete = True pour cet user
        rapports_supprimes = RapportJournalLu.objects.filter(
            user=user,
            is_delete=True
        ).values_list('rapport_id', flat=True)

        rapports = RapportJournal.objects.filter(
            email_destiny__icontains=user.email
        ).exclude(
            id__in=rapports_supprimes  # ← ne pas afficher les supprimés
        ).order_by('-created_at')

        serializer = RapportJournalSerializer(
            rapports, many=True, context={'user': user}
        )
        return Response(serializer.data)


class RapportJournalRecuDetailView(APIView):
    def get(self, request, pk):
        user = getattr(request, 'current_user', None)

        try:
            rapport = RapportJournal.objects.get(
                pk=pk,
                email_destiny__icontains=user.email
            )
        except RapportJournal.DoesNotExist:
            return Response({"error": "Rapport introuvable"}, status=404)

        serializer = RapportJournalSerializer(rapport)
        return Response(serializer.data)
    
class RapportJournalDeleteView(APIView):
    def patch(self, request, pk):
        user = getattr(request, 'current_user', None)
        if not user:
            return Response({"error": "Non authentifié"}, status=401)

        try:
            rapport = RapportJournal.objects.get(
                pk=pk,
                email_destiny__icontains=user.email
            )
        except RapportJournal.DoesNotExist:
            return Response({"error": "Rapport introuvable"}, status=404)

        # Marquer comme supprimé sans supprimer réellement
        lecture, _ = RapportJournalLu.objects.get_or_create(
            rapport=rapport, user=user
        )
        lecture.is_delete = True
        lecture.save()

        return Response({"message": "Email supprimé de votre boîte"})
    
class TextModelCreateView(APIView):
    def post(self, request):
        try:
            text = request.data.get("text")

            if not text:
                return Response(
                    {"error": "Le texte est obligatoire"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            model = TextModel.objects.create(
                text=text
            )

            return Response(
                {
                    "message": "Modèle créé avec succès",
                    "id": model.id,
                    "text": model.text,
                    "create_at": model.create_at
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class TextModelListView(APIView):
    def get(self, request):
        try:
            modeles = TextModel.objects.all().order_by('-create_at')
            data = [
                {
                    "id": m.id,
                    "text": m.text,
                    "create_at": m.create_at
                }
                for m in modeles
            ]
            return Response(data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
class TextModelUpdateView(APIView):
    def put(self, request, pk):
        try:
            modele = TextModel.objects.get(pk=pk)

            modele.text = request.data.get("text")
            modele.save()

            return Response({"message": "modifié"})

        except TextModel.DoesNotExist:
            return Response({"error": "introuvable"}, status=404)
        
class TextModelDeleteView(APIView):
    def delete(self, request, pk):
        try:
            modele = TextModel.objects.get(pk=pk)

            modele.delete()

            return Response({"message": "supprimé"})

        except TextModel.DoesNotExist:
            return Response({"error": "introuvable"}, status=404)
        
class AlerteRapportStockView(APIView):
    def get(self, request):
        try:
            alertes = []

            # Consommables avec qte_restant < 4
            # Prendre la dernière entrée par consommable
            from django.db.models import Max

            derniers = Stock_consommable.objects.values(
                'consommable__id',
                'consommable__nom_consommable'
            ).annotate(
                derniere_date=Max('date_mouvement')
            )

            for item in derniers:
                dernier_stock = Stock_consommable.objects.filter(
                    consommable__id=item['consommable__id'],
                    date_mouvement=item['derniere_date']
                ).first()

                if not dernier_stock:
                    continue

                nom = item['consommable__nom_consommable']

                # Exclure ram/papier — géré séparément en pourcentage
                noms_exclus = ['ram', 'rams', 'papier', 'ram papier']
                if nom.lower() in noms_exclus:
                    continue

                if dernier_stock.qte_restant < 4:
                    alertes.append({
                        "nom": nom,
                        "qte_restant": dernier_stock.qte_restant,
                        "type": "quantite",
                        "message": f"*Alerte : {nom} il ne reste que {dernier_stock.qte_restant} !"
                    })

            # Alerte papier en pourcentage
            try:
                from datetime import datetime, timezone as tz
                from django.db.models import Q, Sum

                stocks_ram = Stock_consommable.objects.filter(
                    Q(consommable__nom_consommable__iexact='ram') |
                    Q(consommable__nom_consommable__iexact='rams') |
                    Q(consommable__nom_consommable__iexact='papier') |
                    Q(consommable__nom_consommable__iexact='ram papier'),
                ).order_by('date_mouvement')

                if stocks_ram.exists():
                    premiere_entree = stocks_ram.filter(qte_entree__gt=0).first()
                    if premiere_entree:
                        now = datetime.now(tz=tz.utc)
                        delta = now - premiere_entree.date_mouvement
                        jours_ecoules = delta.total_seconds() / 86400
                        total_entree = stocks_ram.aggregate(
                            total=Sum('qte_entree')
                        )['total'] or 0
                        pourcentage_total = max(0, (total_entree * 100) - (jours_ecoules * 5))

                        if pourcentage_total < 25:
                            alertes.append({
                                "nom": "papier",
                                "qte_restant": round(pourcentage_total, 2),
                                "type": "pourcentage",
                                "message": f"*Alerte : papier il ne reste que {round(pourcentage_total, 2)}%"
                            })
            except Exception:
                pass

            return Response({"alertes": alertes})

        except Exception as e:
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)