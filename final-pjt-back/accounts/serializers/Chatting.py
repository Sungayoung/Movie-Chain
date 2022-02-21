from django.db.models import fields
from rest_framework import serializers
from accounts.models import User, Chatting
from accounts.serializers.User import UserSerializer


class ChattingSerializer(serializers.ModelSerializer):
    
    class UserSerializer(serializers.ModelSerializer):
        profile_img = serializers.ImageField(use_url=True)

        class Meta:
            model = User
            fields = ('id', 'email', 'nickname', 'profile_img')

    from_user = UserSerializer()
    to_user = UserSerializer()
    created_at = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Chatting
        fields = ('id', 'from_user', 'to_user', 'content', 'created_at', 'is_read')
    