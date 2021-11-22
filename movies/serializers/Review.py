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
    isLiked = serializers.SerializerMethodField()
    isWriter = serializers.SerializerMethodField()

    def get_isLiked(self, obj):
        return obj.like_users.filter(id=self.context.get('user').id).exists()

    def get_isWriter(self, obj):
        return obj.user == self.context.get('user')

    class Meta:
        model = Review
        fields = ('id', 'user', 'content', 'rank',
                  'created_at', 'updated_at', 'isWriter', 'isLiked')
