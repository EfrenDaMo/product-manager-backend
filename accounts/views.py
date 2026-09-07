from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .models import User
from .serializers import UserSerializer, UserCreateSerializer, ChangePasswordSerializer
from .permissions import IsAdmin

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=request.user)
        return Response(serializer.data)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save()
        return Response({"detail": "Password updated."})

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all().order_by("-date_joined")
    permission_classes = [IsAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["role", "is_active"]
    search_fields = ["username", "email"]

    def get_serializer_class(self):
        return UserCreateSerializer if self.request.method == "POST" else UserSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class UserToggleActiveView(APIView):
    permission_classes = [IsAdmin]

    def patch(self, request, pk):
        user = generics.get_object_or_404(User, pk=pk)
        user.is_active = not user.is_active
        user.updated_by = request.user
        user.save()
        return Response(UserSerializer(user).data)
