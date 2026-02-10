from rest_framework import serializers
from accounts.models import QyurateUser

class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return QyurateUser.objects.create_user(**validated_data)
    class Meta:
        model = QyurateUser
        fields = "__all__" 