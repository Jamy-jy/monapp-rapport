from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import traceback
from .models import Systeme, Materiels, Reseau, IncidentSurvenu
from stock_consommables.models import BoxPaf, BoxOp
from myrapport.models import RapportJournal

#systeme
class SystemeListView(APIView):
    def get(self, request):
        try:
            systemes = Systeme.objects.select_related('user').order_by('-date_creation')
            data = [
                {
                    "id": s.id,
                    "titre_systeme": s.titre_systeme,
                    "solution": s.solution_incident_système or '',
                    "fichier_solution": s.fichier_solution.url if s.fichier_solution else None,
                    "date_creation": s.date_creation.strftime('%d %b %Y'),
                    "user_prenom": s.user.prenom if s.user else 'Inconnu',
                }
                for s in systemes
            ]
            return Response(data)
        except Exception as e:
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)


class SystemeCreateView(APIView):
    def post(self, request):
        try:
            titre = request.data.get('titre_systeme', '').strip()
            solution = request.data.get('solution', '').strip()
            fichier = request.FILES.get('fichier_solution')
            user = getattr(request, 'current_user', None)

            if not titre:
                return Response(
                    {"titre_systeme": "Ce champ ne peut pas être vide."},
                    status=400
                )

            systeme = Systeme.objects.create(
                titre_systeme=titre,
                solution_incident_système=solution or None,
                fichier_solution=fichier,
                user=user
            )

            return Response({
                "message": "Incident créé",
                "id": systeme.id,
                "fichier": systeme.fichier_solution.url if systeme.fichier_solution else None,
            }, status=201)

        except Exception as e:
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)


class SystemeUpdateView(APIView):
    def patch(self, request, pk):
        try:
            systeme = Systeme.objects.get(pk=pk)
            titre = request.data.get('titre_systeme', '').strip()
            solution = request.data.get('solution', '').strip()

            if titre:
                systeme.titre_systeme = titre
            systeme.solution_incident_système = solution or None
            systeme.save()

            return Response({"message": "Incident mis à jour"})

        except Systeme.DoesNotExist:
            return Response({"error": "Introuvable"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class SystemeDeleteView(APIView):
    def delete(self, request, pk):
        try:
            systeme = Systeme.objects.get(pk=pk)
            systeme.delete()
            return Response({"message": "Incident supprimé"})
        except Systeme.DoesNotExist:
            return Response({"error": "Introuvable"}, status=404)
        

#Materiel
class MaterielListView(APIView):
    def get(self, request):
        try:
            materiels = Materiels.objects.select_related('user','box_paf','box_op').order_by('-date_creation')
            data = [
                {
                    "id": m.id,
                    "titre_incident": m.titre_incident,
                    "nom_materiel": m.nom_materiel,
                    "box_paf": {
                                "id": m.box_paf.id,
                                "nom": str(m.box_paf),
                            }
                            if m.box_paf
                            else None,
                    "box_op":{ 
                                "id": m.box_op.id,
                                "nom": str(m.box_op),
                            }
                            if m.box_op
                            else None,
                    "solution_incident_materiel": m.solution_incident_materiel or '',
                    "fichier_solution": m.fichier_solution.url if m.fichier_solution else None,
                    "date_creation": m.date_creation.strftime('%d %b %Y'),
                    "user_prenom": m.user.prenom if m.user else 'Inconnu',
                }
                for m in materiels
            ]
            print(data)
            return Response(data)
        except Exception as e:
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)


class MaterielCreateView(APIView):
    def post(self, request):
        try:
            titre_incident = request.data.get('titre_incident', '').strip()
            nom_materiel = request.data.get('nom_materiel', '').strip()
            box_paf_id = request.data.get('box_paf')
            box_op_id = request.data.get('box_op')
            solution = request.data.get('solution', '').strip()
            fichier = request.FILES.get('fichier_solution')
            user = getattr(request, 'current_user', None)

            errors = {}

            if not nom_materiel:
                return Response(
                    {"nom materiel": "Ce champ ne peut pas être vide."},
                    status=400
                )
            
            if not box_paf_id and not box_op_id:
                errors['box'] = "Le matériel doit appartenir à un box."

            if box_paf_id and box_op_id:
                errors['box'] = "Choisissez soit Box Paf soit Box Op."

            if errors:
                return Response(errors, status=400)
            
             # récupération des objets FK
            box_paf = None
            box_op = None

            if box_paf_id:
                try:
                    box_paf = BoxPaf.objects.get(id=box_paf_id)
                except BoxPaf.DoesNotExist:
                    return Response(
                        {"box_paf": "Box Paf introuvable."},
                        status=404
                    )

            if box_op_id:
                try:
                    box_op = BoxOp.objects.get(id=box_op_id)
                except BoxOp.DoesNotExist:
                    return Response(
                        {"box_op": "Box Op introuvable."},
                        status=404
                    )

            materiel = Materiels.objects.create(
                titre_incident=titre_incident,
                nom_materiel=nom_materiel,
                box_paf=box_paf,
                box_op=box_op,
                solution_incident_materiel=solution or None,
                fichier_solution=fichier,
                user=user
            )

            return Response({
                "message": "Incident créé",
                "id": materiel.id,
                "fichier": materiel.fichier_solution.url if materiel.fichier_solution else None,
            }, status=201)

        except Exception as e:
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)


class MaterielUpdateView(APIView):
    def patch(self, request, pk):
        try:
            materiel = Materiels.objects.get(pk=pk)
            titre_incident = request.data.get('titre_incident', '').strip()
            nom_materiel = request.data.get('nom_materiel', '').strip()
            box_paf = request.data.get('box_paf', '').strip()
            box_op = request.data.get('box_op', '').strip()
            solution = request.data.get('solution', '').strip()

            if titre_incident: 
                materiel.titre_incident = titre_incident
            materiel.nom_materiel = nom_materiel
            box_paf=box_paf
            box_op=box_op
            materiel.solution_incident_materiel = solution or None
            materiel.save()

            return Response({"message": "Incident mis à jour"})

        except Materiels.DoesNotExist:
            return Response({"error": "Introuvable"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class MaterielDeleteView(APIView):
    def delete(self, request, pk):
        try:
            materiel = Materiels.objects.get(pk=pk)
            materiel.delete()
            return Response({"message": "Incident supprimé"})
        except Materiels.DoesNotExist:
            return Response({"error": "Introuvable"}, status=404)
        

#reseau
class ReseauListView(APIView):
    def get(self, request):
        try:
            reseaux = Reseau.objects.select_related('user').order_by('-date_creation')
            data = [
                {
                    "id": r.id,
                    "nom_incident_reseau": r.nom_incident_reseau,
                    "solution": r.solution_incident_reseau or '',
                    "fichier_solution": r.fichier_solution.url if r.fichier_solution else None,
                    "date_creation": r.date_creation.strftime('%d %b %Y'),
                    "user_prenom": r.user.prenom if r.user else 'Inconnu',
                }
                for r in reseaux
            ]
            return Response(data)
        except Exception as e:
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)


class ReseauCreateView(APIView):
    def post(self, request):
        try:
            titre = request.data.get('nom_incident_reseau', '').strip()
            solution = request.data.get('solution_incident_reseau', '').strip()
            fichier = request.FILES.get('fichier_solution')
            user = getattr(request, 'current_user', None)

            if not titre:
                return Response(
                    {"nom_incident_reseau": "Ce champ ne peut pas être vide."},
                    status=400
                )

            reseau = Reseau.objects.create(
                nom_incident_reseau=titre,
                solution_incident_reseau=solution or None,
                fichier_solution=fichier,
                user=user
            )

            return Response({
                "message": "Incident créé",
                "id": reseau.id,
                "fichier": reseau.fichier_solution.url if reseau.fichier_solution else None,
            }, status=201)

        except Exception as e:
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)


class ReseauUpdateView(APIView):
    def patch(self, request, pk):
        try:
            reseau = Reseau.objects.get(pk=pk)
            titre = request.data.get('nom_incident_reseau', '').strip()
            solution = request.data.get('solution_incident_reseau', '').strip()

            if titre:
                reseau.nom_incident_reseau = titre
            reseau.solution_incident_reseau = solution or None
            reseau.save()

            return Response({"message": "Incident mis à jour"})

        except Reseau.DoesNotExist:
            return Response({"error": "Introuvable"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class ReseauDeleteView(APIView):
    def delete(self, request, pk):
        try:
            reseau = Reseau.objects.get(pk=pk)
            reseau.delete()
            return Response({"message": "Incident supprimé"})
        except Reseau.DoesNotExist:
            return Response({"error": "Introuvable"}, status=404)

class IncidentsListCombinesView(APIView):
    def get(self, request):
        try:
            incidents = []

             # Systeme
            for s in Systeme.objects.select_related('user').all():
                incidents.append({
                    "id": s.id,
                    "source": "systeme",
                    "titre": s.titre_systeme,
                    "type": "Système",
                    "solution": s.solution_incident_système or '',
                    "fichier_solution": s.fichier_solution.url if s.fichier_solution else None,
                    "date_creation": s.date_creation.strftime('%d %b %Y'),
                    "user_prenom": s.user.prenom if s.user else 'Inconnu',
                })

            # Materiels
            for m in Materiels.objects.select_related('user').all():
                incidents.append({
                    "id": m.id,
                    "source": "materiel",
                    "titre": m.titre_incident or '',
                    "type": f"{m.nom_materiel} (matériel)",
                    "solution": m.solution_incident_materiel or '',
                    "fichier_solution": s.fichier_solution.url if s.fichier_solution else None,
                    "date_creation": m.date_creation.strftime('%d %b %Y'),
                    "user_prenom": m.user.prenom if m.user else 'Inconnu',
                })

            # Reseau
            for r in Reseau.objects.select_related('user').all():
                incidents.append({
                    "id": r.id,
                    "source": "reseau",
                    "titre": r.nom_incident_reseau,
                    "type": "Réseau",
                    "solution": r.solution_incident_reseau or '',
                    "fichier_solution": s.fichier_solution.url if s.fichier_solution else None,
                    "date_creation": r.date_creation.strftime('%d %b %Y'),
                    "user_prenom": r.user.prenom if r.user else 'Inconnu',
                })

            # Trier par titre alphabétique
            incidents.sort(key=lambda x: x['titre'].lower())

            return Response(incidents)

        except Exception as e:
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)

#incident survenu lors de service créer par tech
class IncidentSurvenuCreateView(APIView):
    def post(self, request):
        try:
            nom_incident = request.data.get('nom_incident', '').strip()
            type_incident = request.data.get('type', '').strip()
            #au cas ou le front envoi descrition et solution = Null
            description = request.data.get('description_incident') or ''
            description = description.strip()
            solution = request.data.get('solutionPrise') or ''
            solution = solution.strip()
            user = getattr(request, 'current_user', None)

            errors = {}

            if not nom_incident:
                errors['nom_incident'] = 'Ce champ ne peut pas être vide.'
            if not type_incident:
                errors['type'] = 'Veuillez choisir un type.'
            if type_incident not in ['systeme', 'materiel', 'reseau']:
                errors['type'] = 'Type invalide.'

            if errors:
                return Response(errors, status=400)

            incident = IncidentSurvenu.objects.create(
                nom_incident=nom_incident,
                type=type_incident,
                description_incident=description or None,
                solutionPrise=solution or None,
                user=user,
            )

            return Response({
                "message": "Incident enregistré",
                "id": incident.id,
            }, status=201)

        except Exception as e:
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)
        
class DernierIncidentUserView(APIView):
    def get(self, request):
        try:
            user = getattr(request, 'current_user', None)
            if not user:
                return Response({"error": "Non authentifié"}, status=401)

             # Récupérer l'ID du dernier rapport envoyé par cet user
            dernier_rapport = RapportJournal.objects.filter(
                user=user
            ).order_by('-created_at').first()

            # Tous les incidents créés APRÈS le dernier rapport envoyé
            if dernier_rapport:
                incidents = IncidentSurvenu.objects.filter(
                    user=user,
                    date_creation__gt=dernier_rapport.created_at
                ).order_by('date_creation')
            else:
                # Aucun rapport envoyé → tous les incidents
                incidents = IncidentSurvenu.objects.filter(
                    user=user
                ).order_by('date_creation')

            data = [
                {
                    "id": i.id,
                    "nom_incident": i.nom_incident,
                    "type": i.type,
                    "description_incident": i.description_incident or '',
                    "solutionPrise": i.solutionPrise or '',
                    "date_creation": i.date_creation.strftime('%d %b %Y %H:%M'),
                }
                for i in incidents
            ]

            print("incident", data)
            
            return Response({"incident": data})

        except Exception as e:
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)

class TechlistIncidentSurvenuView(APIView):
    def get(self, request):
        try:
            incidents = []

            for i in IncidentSurvenu.objects.select_related('user').all():
                incidents.append({
                    "id": i.id,
                    "nom_incident": i.nom_incident,
                    "type": i.type,
                    "description_incident": i.description_incident or '',
                    "date_creation": i.date_creation.strftime('%d %b %Y %H:%M'),
                    "user_prenom": i.user.prenom if i.user else 'Inconnu',
                })

            return Response(incidents)
        
        except Exception as e:
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)

class SearchTechIncidentView(APIView):
    def get(self, request):
        try:
            tech_id = request.GET.get('tech', '')
            date_debut = request.GET.get('dateDebut', '')
            date_fin = request.GET.get('dateFin', '')

            incidents = IncidentSurvenu.objects.select_related('user').all()

            # Filtre par technicien
            if tech_id:
                incidents = incidents.filter(user__id=tech_id)

            # Filtre par date début
            if date_debut:
                from django.utils.dateparse import parse_datetime
                from django.utils.timezone import make_aware
                dt_debut = parse_datetime(date_debut)
                if dt_debut and dt_debut.tzinfo is None:
                    dt_debut = make_aware(dt_debut)
                if dt_debut:
                    incidents = incidents.filter(date_creation__gte=dt_debut)

            # Filtre par date fin
            if date_fin:
                dt_fin = parse_datetime(date_fin)
                if dt_fin and dt_fin.tzinfo is None:
                    dt_fin = make_aware(dt_fin)
                if dt_fin:
                    incidents = incidents.filter(date_creation__lte=dt_fin)

            incidents = incidents.order_by('-date_creation')

            data = [
                {
                    "id": i.id,
                    "nom_incident": i.nom_incident,
                    "type": i.get_type_display(),
                    "description_incident": i.description_incident or '',
                    "solutionPrise": i.solutionPrise or '',
                    "user_prenom": f"{i.user.prenom} {i.user.nom}" if i.user else 'Inconnu',
                    "user_id": i.user.id if i.user else None,
                    "date_creation": i.date_creation.strftime('%d %b %Y %H:%M'),
                }
                for i in incidents
            ]

            return Response(data)

        except Exception as e:
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)
# Create your views here.
