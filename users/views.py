from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model

from users.permissions import IsAdminUser
from .serializers import UserSerializer, RegisterSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """
    User controller/ endpoints.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):  # Make the predefined method in ModelViewSet custom
        """
        List users for is_admin = True only
        """
        self.permission_classes = [IsAdminUser]
        self.check_permissions(request)  # Check if the current user is admin
        return super().list(request)
    
    def retrieve(self, request, pk=None):
        """
        Permit get any user information only for is_admin = True
        """
        user = self.get_object()
        if request.user.is_admin or request.user == user:
            super().retrieve(request, pk)
        return Response(status=status.HTTP_403_FORBIDDEN, data={'detail': 'Access is prohibited'})

    @action(
        detail=False,
        methods=['POST'],
        url_path='register',
        permission_classes=[AllowAny]
    )
    def register(self, request):
        """
        A new user registration
        """
        serializer = RegisterSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(
        detail=False,
        methods=['GET'],
        url_path='me',
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        serializer = serializer.get_serializer(request.user)
        return Response(serializer.data)
    
    def get_permissions(self):
        if self.action in ['register']:
            self.permission_classes = [AllowAny]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return super(UserViewSet, self).get_permissions()