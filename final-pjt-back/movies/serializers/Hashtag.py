from movies.models import Hashtag
from rest_framework import serializers

class HashtagSerializer(serializers.ModelSerializer):
        class Meta:
            model = Hashtag
            fields = '__all__'