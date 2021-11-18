from re import T
from rest_framework import serializers
from movies.models import Review
from accounts.models import User


class ReviewSerializer(serializers.ModelSerializer):

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('nickname', 'profile_img')

    user = UserSerializer(read_only=True)
    like_users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = ('pk', 'user', 'content', 'rank',
                  'created_at', 'updated_at', 'like_users')
