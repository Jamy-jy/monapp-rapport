from rest_framework import serializers
from .models import Conversation, ConversationMember, Message

class MemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    role = serializers.CharField(source='user.role')
    class Meta:
        model = ConversationMember
        fields = ['user_id', 'username', 'role']

class ConversationSerializer(serializers.ModelSerializer):
    # members = MemberSerializer(many=True, read_only=True)
    members      = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'name', 'type', 'created_at', 'members', 'last_message']

    def get_members(self, obj):
        return [
            {
                'user_id':  m.user.id,
                'username': f"{m.user.prenom} {m.user.nom}",
                'role':     m.user.role,
            }
            for m in obj.members.select_related('user').all()
        ]
    
    # def get_last_message(self, obj):
    #     msg = obj.messages.last()
    #     return MessageSerializer(msg).data if msg else None

    def get_last_message(self, obj):
        msg = obj.messages.order_by('-sent_at').first()
        if not msg:
            return None
        return {
            'id':          msg.id,
            'content':     msg.content,
            'sent_at':     msg.sent_at,
            'sender_name': f"{msg.sender.prenom} {msg.sender.nom}",
            'sender_role': msg.sender.role,
        }
    
class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    sender_role = serializers.SerializerMethodField()
    sender_id   = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'content', 'sent_at', 'sender_id', 'sender_name', 'sender_role']
        read_only_fields = ['sent_at']

    def get_sender_name(self, obj):
        return f"{obj.sender.prenom} {obj.sender.nom}" if obj.sender else ''

    def get_sender_role(self, obj):
        return obj.sender.role if obj.sender else ''

    def get_sender_id(self, obj):
        return obj.sender.id if obj.sender else None
    
class CreateGroupSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    tech_ids = serializers.ListField(child=serializers.IntegerField(), min_length=1)