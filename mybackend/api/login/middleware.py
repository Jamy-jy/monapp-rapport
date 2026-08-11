import jwt
from django.conf import settings


BLACKLISTED_TOKENS = set()

class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Routes publiques — pas besoin de token
        public_routes = ['/api/login', '/admin/', '/upload', '/media']
        if any(request.path.startswith(route) for route in public_routes):
            return self.get_response(request)

        token = request.headers.get('Authorization', '').replace('Bearer ', '')

        if not token:
            from django.http import JsonResponse
            return JsonResponse(
                {"error": "Token manquant"},
                status=401
            )
        
        if token in BLACKLISTED_TOKENS:
            from django.http import JsonResponse
            return JsonResponse({"error": "Session expirée"}, status=401)

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            from users.models import User
            request.current_user = User.objects.get(id=payload['user_id'])
        except jwt.ExpiredSignatureError:
            from django.http import JsonResponse
            return JsonResponse({"error": "Token expiré"}, status=401)
        except Exception:
            from django.http import JsonResponse
            return JsonResponse({"error": "Token invalide"}, status=401)

        return self.get_response(request)