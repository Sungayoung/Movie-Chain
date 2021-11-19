from django.db.models import fields
from rest_framework import serializers
from accounts.models import User, Chatting
from accounts.serializers.User import UserSerializer


class ChattingSerializer(serializers.ModelSerializer):

    from_user = UserSerializer()
    to_user = UserSerializer()
    created_at = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Chatting
        fields = ('from_user', 'to_user', 'content', 'created_at')
    