from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        nom = request.data.get('nom', '').strip()
        prenom = request.data.get('prenom', '').strip()
        email = request.data.get('email', '').strip()
        role = request.data.get('role', 'tech')
        password = request.data.get('password', '')
        phone = request.data.get('phone', '').strip()

        errors = {}

        # Email unique
        if email and User.objects.filter(email=email).exists():
            errors['email'] = "Cet email est déjà utilisé"

        # Mot de passe > 6 caractères
        if password and len(password) < 6:
            errors['password'] = "Le mot de passe doit contenir au moins 6 caractères"

        # Phone — exactement 10 chiffres
        phone_digits = phone.replace(' ', '')
        if phone and (not phone_digits.isdigit() or len(phone_digits)) != 10:
            errors['phone'] = "Le numéro doit contenir exactement 10 chiffres"

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        # Utilisation du serializer (important pour cohérence)
        serializer = self.get_serializer(data={
            "nom": nom,
            "prenom": prenom,
            "email": email,
            "role": role,
            "phone": phone,
            "password": password
        })

        user = User(
            nom=nom,
            prenom=prenom,
            email=email,
            role=role,
            phone=phone
        )
        
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "message": "Utilisateur créé",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    

    def update(self, request, *args, **kwargs):
        try:
            user = self.get_object()
        except User.DoesNotExist:
            return Response(
                {"error": "Utilisateur introuvable"},
                status=status.HTTP_404_NOT_FOUND
            )

        nom = request.data.get('nom', '').strip()
        prenom = request.data.get('prenom', '').strip()
        email = request.data.get('email', '').strip()
        role = request.data.get('role', '')
        phone = request.data.get('phone', '').strip()
        password = request.data.get('password', '')

        errors = {}

        # Email unique en excluant l'utilisateur actuel
        if email and User.objects.filter(email=email).exclude(pk=user.pk).exists():
            errors['email'] = "Cet email est déjà utilisé"

        # Phone
        if phone:
            phone_digits = phone.replace(' ', '')
            if not phone_digits.isdigit() or len(phone_digits) != 10:
                errors['phone'] = "Le numéro doit contenir exactement 10 chiffres"

        # Password optionnel à l'update
        if password and len(password) <= 6:
            errors['password'] = "Le mot de passe doit contenir plus de 6 caractères"

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        # Mise à jour uniquement les champs envoyés
        if nom:
            user.nom = nom
        if prenom:
            user.prenom = prenom
        if email:
            user.email = email
        if role:
            user.role = role
        if phone:
            user.phone = phone
        if password:
            user.set_password(password)

        user.save()

        return Response({
            "message": "Utilisateur mis à jour",
            "data": UserSerializer(user).data
        }, status=status.HTTP_200_OK)

    # TOGGLE STATUT — activer/désactiver compte
    @action(detail=True, methods=['patch'], url_path='toggle-statut')
    def toggle_statut(self, request, pk=None):
        try:
            user = self.get_object()
        except User.DoesNotExist:
            return Response(
                {"error": "Utilisateur introuvable"},
                status=status.HTTP_404_NOT_FOUND
            )

        user.statut = not user.statut  # bascule true/false
        user.save()

        etat = "activé" if user.statut else "désactivé"

        return Response({
            "message": f"Compte {etat}",
            "statut": user.statut,
            "data": UserSerializer(user).data
        }, status=status.HTTP_200_OK)

class TechListView(APIView):
    def get(self, request):
        techs = User.objects.filter(role='tech')

        data = [
            {
                "value": tech.id,
                "label": f"{tech.prenom} {tech.nom}"
            }
            for tech in techs
        ]

        return Response(data)
# Create your views here.
