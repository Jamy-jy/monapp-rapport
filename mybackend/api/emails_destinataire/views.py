from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Emails_destinataire
from .serializers import emails_destinataireSerializer

class emails_destinataireViewset(viewsets.ModelViewSet):
    queryset = Emails_destinataire.objects.all()
    serializer_class = emails_destinataireSerializer

    def create(self, request, *args, **kwargs):
        nom = request.data.get('nom_proprietaire', '').strip()
        email_d = request.data.get('emails_destiny', '').strip()

        errors = {}

        if not nom:
            errors['nom_proprietaire'] = "Le nom est obligatoire"
        if not email_d:
            errors['emails_destiny'] = "Le type est obligatoire"

        # Nom unique
        if email_d and Emails_destinataire.objects.filter(nom_proprietaire__iexact=email_d).exists():
            errors['emails_destiny'] = "Ce email existe déjà"

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        email = Emails_destinataire.objects.create(
            nom_proprietaire=nom,
            emails_destiny=email_d,
            )

        return Response({
            "message": "email créé",
            "data": emails_destinataireSerializer(email).data
        }, status=status.HTTP_201_CREATED)

    # UPDATE
    def update(self, request, *args, **kwargs):
        try:
            email = self.get_object()
        except Emails_destinataire.DoesNotExist:
            return Response(
                {"error": "email introuvable"},
                status=status.HTTP_404_NOT_FOUND
            )

        nom = request.data.get('nom_proprietaire', '').strip()
        email_d = request.data.get('emails_destiny', '').strip()

        errors = {}

        # Nom unique en excluant l'actuel
        if email_d and Emails_destinataire.objects.filter(
            emails_destiny__iexact=email_d
        ).exclude(pk=email.pk).exists():
            errors['emails_destiny'] = "Ce email existe déjà"

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        if nom:
            email.nom_proprietaire = nom
        if email_d:
            email.emails_destiny = email_d

        email.save()

        return Response({
            "message": "email mis à jour",
            "data": emails_destinataireSerializer(email).data
        }, status=status.HTTP_200_OK)

    # DELETE
    def destroy(self, request, *args, **kwargs):
        try:
            email = self.get_object()
            email.delete()
            return Response(
                {"message": "email supprimé"},
                status=status.HTTP_200_OK
            )
        except email.DoesNotExist:
            return Response(
                {"error": "email introuvable"},
                status=status.HTTP_404_NOT_FOUND
            )

# Create your views here.
