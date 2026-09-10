import requests          
import os               
import messagebird
from django.conf import settings
from django.db import models
from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Conversation, ConversationMember, Message, ConversationType
from .serializers import ConversationSerializer, MessageSerializer, CreateGroupSerializer

# --- Permissions custom ------------------------------------------------------
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
            user = getattr(request, 'current_user', None)
            return user is not None and user.role == 'admin'

class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return getattr(request, 'current_user', None) is not None
    
class IsMember(permissions.BasePermission):
    """L'utilisateur est membre de la conversation."""
    def has_object_permission(self, request, view, obj):
        user = get_user(request)
        if not user:
            return False
        return obj.members.filter(user_id=user.id).exists()
    
def get_user(request):
    return getattr(request, 'current_user', None)

# --- Espace commun admins ------------------------------------------------------
@api_view(['GET'])
#@permission_classes([IsAdmin])
def shared_admin_conversation(request):
    """Retourne (ou crée) la conversation partagée entre tous les admins."""
    user = get_user(request)
    if not user or user.role != 'admin':
        return Response({'detail': 'Accès refusé'}, status=403)

    from users.models import User
    conv, created = Conversation.objects.get_or_create(
        type=ConversationType.SHARED_ADMIN,
        defaults={'name': 'Espace admins', 'created_by': user}
    )
    if created:
        # Ajoute tous les admins existants
        admins = user.objects.filter(role='admin')
        ConversationMember.objects.bulk_create(
            [ConversationMember(conversation=conv, user=u) for u in admins]
        )
    return Response(ConversationSerializer(conv, context={'request': request}).data)

# --- Liste des conversations de l'utilisateur connecté ----------------------

@api_view(['GET'])
#  @permission_classes([permissions.IsAuthenticated])
def my_conversations(request):
    user = get_user(request)
    if not user:
        return Response({'detail': 'Non authentifié'}, status=401)
    
    conv_ids = ConversationMember.objects.filter(
        user=user
    ).values_list('conversation_id', flat=True)

    convs = Conversation.objects.filter(id__in=conv_ids)
    return Response(ConversationSerializer(convs, many=True, context={'request': request}).data)

# --- Conversation privée admin - tech ---------------------------------------

@api_view(['POST'])
# --- @permission_classes([IsAdmin])
def create_private_conversation(request): 
    """
    Body: { "tech_ids": [1, 2, 3] }
    Crée une conv privée pour chaque tech sélectionné (ou retrouve l'existante).
    """
    user = get_user(request)
    if not user or user.role != 'admin':
        return Response({'detail': 'Accès refusé'}, status=403)

    print('USER:', user)
    print('ROLE:', user.role)

    tech_ids = request.data.get('tech_ids', [])
    if not tech_ids:
        return Response({'detail': 'tech_ids requis.'}, status=400)

    from users.models import User
    results = []

    for tech_id in tech_ids:
        #  Tech = request.user.__class__
        tech = get_object_or_404(User, id=tech_id, role='tech')

        # code avant 
        # Retrouve une conv privée existante entre cet admin et ce tech
        # existing = Conversation.objects.filter(
        #     type=ConversationType.PRIVATE,
        #     members__user_id=user.id
        # ).filter(members__user_id=tech.id).first()

        # Nouvel code à tester
        # >>> FIX : on cherche une conv privée existante pour ce tech,
        # peu importe QUEL admin en est membre (avant : restreint à user.id)
        existing = Conversation.objects.filter(
            type=ConversationType.PRIVATE,
            members__user_id=tech.id
        ).distinct().first()

        if existing:
            results.append(ConversationSerializer(existing, context={'request': request}).data)
            continue

        # code avant
        # conv = Conversation.objects.create(
        #     name=f"{user.prenom} {user.nom} - {tech.prenom} {tech.nom}",
        #     type=ConversationType.PRIVATE,
        #     created_by=user
        # )
        # ConversationMember.objects.bulk_create([
        #     ConversationMember(conversation=conv, user=user),
        #     ConversationMember(conversation=conv, user=tech),
        # ])

        # Nouvel code à tester
        conv = Conversation.objects.create(
            name=f"Admin - {tech.prenom} {tech.nom}",  # >>> FIX : nom neutre, plus lié à un seul admin
            type=ConversationType.PRIVATE,
            created_by=user
        )

        # >>> FIX : on ajoute TOUS les admins comme membres, pas seulement user
        admins = User.objects.filter(role='admin')
        members = [ConversationMember(conversation=conv, user=a) for a in admins]
        members.append(ConversationMember(conversation=conv, user=tech))
        ConversationMember.objects.bulk_create(members)

        results.append(ConversationSerializer(conv, context={'request': request}).data)
   

    return Response(results, status=201)

# --- Créer un groupe -----------------------------------------------------

@api_view(['POST'])
# @permission_classes([IsAdmin])
def create_group(request):
    """
    Body: { "name": "Équipe infra", "tech_ids": [1, 2, 3] }
    """
    user = get_user(request)

    print("USER CREATE GROUP:", user)

    if not user or user.role != 'admin':
        return Response({'detail': 'Accès refusé'}, status=403)
    
    # serializer = CreateGroupSerializer(data=request.data)
    # serializer.is_valid(raise_exception=True)

    name = request.data.get('name', '').strip()
    tech_ids = request.data.get('tech_ids', [])

    if not name:
        return Response({'detail': 'name requis.'}, status=400)
    if not tech_ids:
        return Response({'detail': 'tech_ids requis.'}, status=400)

    from users.models import User
    
    conv = Conversation.objects.create(
        name=name,
        type=ConversationType.GROUP,
        created_by=user
    )
    # L'admin créateur + les techs sélectionnés
    members = [ConversationMember(conversation=conv, user=user)]
    # Tech = request.user.__class__
    for tech in User.objects.filter(id__in=tech_ids, role='tech'):
        members.append(ConversationMember(conversation=conv, user=tech))
    ConversationMember.objects.bulk_create(members)

    return Response(ConversationSerializer(conv, context={'request': request}).data, status=201)

# --- envoie d'une seul message à plusieur tech ----------------------------

@api_view(['POST'])
# @permission_classes([IsAdmin])
def broadcast_message(request):
    """
    Envoie le même message à plusieurs techs en une seule requête.
    Crée les conversations privées si elles n'existent pas encore.

    Body: {
        "tech_ids": [1, 2, 3],
        "content": "Intervention prévue demain à 9h"
    }
    """
    user = get_user(request)
    if not user or user.role != 'admin':
        return Response({'detail': 'Accès refusé'}, status=403)
    
    tech_ids = request.data.get('tech_ids', [])
    content  = request.data.get('content', '').strip()

    if not tech_ids:
        return Response({'detail': 'tech_ids requis.'}, status=400)
    if not content:
        return Response({'detail': 'content requis.'}, status=400)

    from users.models import User
    techs = User.objects.filter(id__in=tech_ids, role='tech')
    results = []

    # Tech    = request.user.__class__
    # techs   = Tech.objects.filter(id__in=tech_ids, role='tech')
    # results = []

    for tech in techs:
        # code avant
        # filter par user_id ou cree si nouvel
        # conv = Conversation.objects.filter(
        #     type=ConversationType.PRIVATE,
        #     members__user_id=user.id
        # ).filter(members__user_id=tech.id).first()

        # nouvel code à tester
        # >>> FIX : recherche par tech uniquement, plus par (user, tech)
        conv = Conversation.objects.filter(
            type=ConversationType.PRIVATE,
            members__user_id=tech.id
        ).distinct().first()

        if not conv:
            # code avant
            # conv = Conversation.objects.create(
            #     name=f"{user.prenom} {user.nom} - {tech.prenom} {tech.nom}",
            #     type=ConversationType.PRIVATE,
            #     created_by=user
            # )
            # ConversationMember.objects.bulk_create([
            #     ConversationMember(conversation=conv, user=user),
            #     ConversationMember(conversation=conv, user=tech),
            # ])

            # nouvel code à tester
            conv = Conversation.objects.create(
                name=f"Admin - {tech.prenom} {tech.nom}",
                type=ConversationType.PRIVATE,
                created_by=user
            )
            # >>> FIX : tous les admins deviennent membres, pas seulement l'expéditeur du broadcast
            admins = User.objects.filter(role='admin')
            members = [ConversationMember(conversation=conv, user=a) for a in admins]
            members.append(ConversationMember(conversation=conv, user=tech))
            ConversationMember.objects.bulk_create(members)

        # Crée le message dans cette conversation
        msg = Message.objects.create(
            conversation=conv,
            sender=user,
            content=content
        )
        results.append({
            'conversation_id': conv.id,
            'tech': f"{tech.prenom} {tech.nom}",
            'message_id': msg.id,
            'sent_at': msg.sent_at,
        })

    return Response(results, status=201)

# --- Messages d'une conversation --------------------------------------------

class MessageListCreate(generics.ListCreateAPIView):
    serializer_class   = MessageSerializer
    #permission_classes = [permissions.IsAuthenticated]
    permission_classes = [] # géré manuellement

    def get_conversation(self):
        user = get_user(self.request)
        if not user:
            self.permission_denied(self.request)
        conv = get_object_or_404(Conversation, pk=self.kwargs['conv_id'])
        if not conv.members.filter(user_id=user.id).exists():
            self.permission_denied(self.request)
        return conv

    def get_queryset(self):
        return Message.objects.filter(conversation=self.get_conversation())

    # def perform_create(self, serializer):
    #     conv = self.get_conversation()
    #     user = self.request.user
    #     # Un tech ne peut répondre que dans ses propres conversations
    #     if user.role == 'tech' and not conv.members.filter(user=user).exists():
    #         self.permission_denied(self.request)
    #     serializer.save(sender=user, conversation=conv)

    def create(self, request, *args, **kwargs):
        print("REQUEST DATA:", request.data)
        user = get_user(self.request)
        print("USER:", user)
        conv = self.get_conversation()

        msg = Message.objects.create(
            conversation=conv,
            sender=user,
            content=request.data.get('content', '').strip()
        )

        if not msg.content:
            return Response({"content": "Le message ne peut pas être vide."}, status=400)

        return Response(MessageSerializer(msg).data, status=201)
    
@api_view(['POST'])
def send_sms(request):
    user = get_user(request)
    if not user or user.role != 'admin':
        return Response({'detail': 'Accès refusé'}, status=403)

    tech_ids = request.data.get('tech_ids', [])
    content  = request.data.get('content', '').strip()

    if not tech_ids:
        return Response({'detail': 'tech_ids requis.'}, status=400)
    if not content:
        return Response({'detail': 'content requis.'}, status=400)

    from users.models import User
    techs = User.objects.filter(id__in=tech_ids, role='tech')
    results = []
    errors  = []

    # >>> FIX : client officiel messagebird (legacy), lit la clé passée en argument
    client = messagebird.Client(settings.MESSAGEBIRD_API_KEY)

    for tech in techs:
        # Vérifier que le tech a un numéro
        if not tech.phone:
            errors.append({
                'tech': f"{tech.prenom} {tech.nom}",
                'error': 'Numéro de téléphone manquant'
            })
            continue

        # Nettoyer le numéro — retirer espaces
        phone = tech.phone.replace(' ', '').replace('-', '')

        # Ajouter indicatif si manquant (Madagascar +261)
        if not phone.startswith('+'):
            if phone.startswith('0'):
                phone = '+261' + phone[1:]  # 034... -> +261 34...
            else:
                phone = '+261' + phone
        
        print("PHONE:", phone)
        print("API KEY:", settings.MESSAGEBIRD_API_KEY)



        try:
            # url = 'https://eu1.platform.bird.com/v1/sms/messages'  # >>> FIX : "v1/sms" au lieu de "sms/v1" (ordre inversé)
            # print("URL ENVOI:", url)

            # print("HTTP_PROXY:", os.environ.get('HTTP_PROXY', 'None'))
            # print("HTTPS_PROXY:", os.environ.get('HTTPS_PROXY', 'None'))

            response = client.message_create(
                originator=settings.MESSAGEBIRD_ORIGINATOR,
                recipients=[phone],
                body=content
                # url,
                # headers={
                #     'Authorization': f"Bearer {settings.MESSAGEBIRD_API_KEY}",
                #     'Content-Type': 'application/json',  # >>> FIX : "application/json" au lieu de form-urlencoded (Bird attend du JSON, cf. plus bas on utilise déjà json=)
                #     'Accept': 'application/json',
                # },
                # json={
                #     'to': phone,                              # >>> FIX : "to" au lieu de "recipients" (nouveau nom de champ Bird)
                #     'from': settings.MESSAGEBIRD_ORIGINATOR,   # >>> FIX : "from" au lieu de "originator"
                #     'text': content,                           # >>> FIX : "text" au lieu de "body"
                #     'category': 'transactional',               # >>> AJOUT : obligatoire chez Bird (transactional/marketing/authentication/service)
                # },
                # proxies={'http': None, 'https': None},
                # timeout=20
            )
            results.append({
                'tech': f"{tech.prenom} {tech.nom}",
                'phone': phone,
                'status': 'envoyé',
                'message_id': response.id,
            })
            # print("STATUS:", response.status_code)
            # print("RESPONSE:", response.text)

            # if response.text:
            #     resp_json = response.json()
            # else:
            #     resp_json = {}

            # if response.status_code == 202:  # >>> FIX : Bird renvoie 202 (accepté, traitement async), pas 200/201
            #     results.append({
            #         'tech': f"{tech.prenom} {tech.nom}",
            #         'phone': phone,
            #         'status': 'envoyé'
            #     })
            # else:
            #     # >>> FIX : nouvelle structure d'erreur Bird : {"error": {"message": "...", ...}}
            #     # au lieu de l'ancienne {"errors": [{"description": "..."}]}
            #     error_msg = resp_json.get('error', {}).get('message', 'Erreur inconnue')
            #     errors.append({
            #         'tech': f"{tech.prenom} {tech.nom}",
            #         'phone': phone,
            #         'error': error_msg
            #     })

            # print("PHONE:", phone)
            
        except messagebird.client.ErrorException as e:  # >>> FIX : "ErrorException" (faute de frappe corrigée dans le nom de l'exception)
            errors.append({
                'tech': f"{tech.prenom} {tech.nom}",
                'phone': phone,
                'error': str(e.errors[0].description) if e.errors else str(e)
            })
        # except requests.exceptions.Timeout:
        #     errors.append({'tech': f"{tech.prenom} {tech.nom}", 'error': 'Délai dépassé'})
        # except Exception as e:
        #     errors.append({'tech': f"{tech.prenom} {tech.nom}", 'error': str(e)})
    return Response({
        'results': results,
        'errors': errors,
        'total_envoye': len(results),
        'total_erreur': len(errors),
    }, status=200)

# Ajouter un membre au groupe
@api_view(['POST'])
def add_member(request, conv_id):
    user = get_user(request)
    if not user or user.role != 'admin':
        return Response({'detail': 'Accès refusé'}, status=403)

    conv = get_object_or_404(Conversation, pk=conv_id)
    if conv.type not in [ConversationType.GROUP, ConversationType.SHARED_ADMIN]:
        return Response({'detail': 'Opération non autorisée sur ce type de conversation'}, status=400)

    user_id = request.data.get('user_id')
    if not user_id:
        return Response({'detail': 'user_id requis'}, status=400)

    from users.models import User as CustomUser
    member = get_object_or_404(CustomUser, id=user_id)

    _, created = ConversationMember.objects.get_or_create(
        conversation=conv,
        user=member
    )

    if not created:
        return Response({'detail': 'Déjà membre'}, status=400)

    return Response({'message': f"{member.prenom} {member.nom} ajouté"}, status=201)


# Retirer un membre du groupe
@api_view(['DELETE'])
def remove_member(request, conv_id, user_id):
    user = get_user(request)
    if not user or user.role != 'admin':
        return Response({'detail': 'Accès refusé'}, status=403)

    conv = get_object_or_404(Conversation, pk=conv_id)

    from users.models import User as CustomUser
    member = get_object_or_404(CustomUser, id=user_id)

    # Ne pas retirer le créateur
    if conv.created_by and conv.created_by.id == member.id:
        return Response({'detail': 'Impossible de retirer le créateur'}, status=400)

    deleted, _ = ConversationMember.objects.filter(
        conversation=conv,
        user_id=user_id
    ).delete()

    if not deleted:
        return Response({'detail': 'Membre introuvable'}, status=404)

    return Response({'message': f"{member.prenom} {member.nom} retiré"})


# Supprimer une conversation
@api_view(['DELETE'])
def delete_conversation(request, conv_id):
    user = get_user(request)
    if not user or user.role != 'admin':
        return Response({'detail': 'Accès refusé'}, status=403)

    conv = get_object_or_404(Conversation, pk=conv_id)
    conv.delete()

    return Response({'message': 'Conversation supprimée'})


# Supprimer un message
@api_view(['DELETE'])
def delete_message(request, conv_id, msg_id):
    user = get_user(request)
    if not user:
        return Response({'detail': 'Non authentifié'}, status=401)

    msg = get_object_or_404(Message, pk=msg_id, conversation_id=conv_id)

    # Seul l'expéditeur ou un admin peut supprimer
    if msg.sender_id != user.id and user.role != 'admin':
        return Response({'detail': 'Accès refusé'}, status=403)

    msg.delete()
    return Response({'message': 'Message supprimé'})
# Create your views here.
