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
    commentCnt = serializers.SerializerMethodField()
    def get_commentCnt(self, obj):
        return obj.comment_set.count()
    
    def get_isWriter(self, obj):
        return obj.user == self.context.get('user')

    def get_isLiked(self, obj):
        return obj.like_users.filter(id=self.context.get('user').id).exists()

    class Meta:
        model = Review
        fields = ('id', 'user', 'content', 'rank',
                  'created_at', 'updated_at', 'isLiked', 'isWriter', 'commentCnt')
