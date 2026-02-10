# views.py

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from accounts.models import QyurateUser
from accounts.serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = QyurateUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    def register(self, request):
        data={}
        data['username'] = request.data.get('email')
        data['password'] = request.data.get('password')
        data['email'] = request.data.get('email')
        user_serializer = self.serializer_class(data=data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)