from rest_framework import serializers
from movies.models import Comment
from accounts.models import User

# 댓글보기를 누를 경우에만 리뷰댓글을 불러와야 하므로 serializer 분리


class CommentSerializer(serializers.ModelSerializer):

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('nickname', 'profile_img')

    user = UserSerializer(read_only=True)
    isWriter = serializers.SerializerMethodField()

    def get_isWriter(self, obj):
        return obj.user == self.context.get('user')

    class Meta:
        model = Comment
        fields = ('id', 'user', 'content', 'isWriter', 'created_at', 'updated_at')
