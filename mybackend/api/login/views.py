from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
import jwt
import datetime
from django.conf import settings
from users.models import User

BLACKLISTED_TOKENS = set()

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {"error": "Email et mot de passe requis"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "Identifiants incorrects"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Vérif mot de passe
        if not user.check_password(password):
            return Response(
                {"error": "Identifiants incorrects"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Vérif compte actif
        if not user.statut:
            return Response(
                {"error": "Compte désactivé"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Marquer en ligne
        user.actif = True
        user.save()

        # Génération token JWT
        payload = {
            'user_id': user.id,
            'email': user.email,
            'nom': user.nom,
            'prenom': user.prenom,
            'role': user.role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8),
            'iat': datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return Response({
            "token": token,
            "user": {
                "id": user.id,
                "nom": user.nom,
                "prenom": user.prenom,
                "email": user.email,
                "role": user.role,
            }
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    def post(self, request):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')

        if not token:
            return Response({"error: token manquand"}, statur=400)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            #Blacklister le token
            BLACKLISTED_TOKENS.add(token)
            user = User.objects.get(id=payload['user_id'])
            user.actif = False
            user.save()
        except Exception:
            pass
        return Response({"message": "Déconnecté"}, status=status.HTTP_200_OK)
    
class CheckStatutView(APIView):
    def get(self, request):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not token:
            return Response({"error": "Token manquant"}, status=401)
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            
            if not user.statut:
                return Response({"statut": False, "error": "Compte bloqué"}, status=403)
            
            return Response({"statut": True}, status=200)
            
        except jwt.ExpiredSignatureError:
            return Response({"error": "Token expiré"}, status=401)
        except Exception:
            return Response({"error": "Token invalide"}, status=401)
# Create your views here.
