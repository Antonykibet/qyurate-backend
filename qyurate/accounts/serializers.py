from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from accounts.models import QyurateUser

class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return QyurateUser.objects.create_user(**validated_data)
    class Meta:
        model = QyurateUser
        fields = "__all__" 

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['is_staff'] = user.is_staff
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['is_staff'] = self.user.is_staff
        return data
    