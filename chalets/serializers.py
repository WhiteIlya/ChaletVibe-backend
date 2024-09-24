from rest_framework import serializers
from .models import Chalet, UserReaction

class ChaletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chalet
        fields = '__all__'
        read_only_fields = ['id']

class UserReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReaction
        fields = ['user', 'chalet', 'liked']
        read_only_fields = ['user']