from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from .serializers import (
    LoginSerializer, RegisterDriverSerializer,
    UserSerializer, CreateUserSerializer, GroupSerializer, PermissionSerializer,
    RegisterCustomerSerializer,
)
from . import services
from apps.drivers.services import create_driver_with_user
from apps.drivers.serializers import DriverSerializer


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        token = services.login(
            serializer.validated_data['username'],
            serializer.validated_data['password'],
        )
        if token is None:
            return Response({'detail': 'Credenciales inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)
        user = token.user
        return Response({
            'token': token.key,
            'is_superuser': user.is_superuser,
            'username': user.username,
            'first_name': user.first_name,
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        services.logout(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegisterDriverView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterDriverSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        user_data = {
            'username': data['username'],
            'password': data['password'],
            'email': data.get('email', ''),
            'first_name': data.get('first_name', ''),
            'last_name': data.get('last_name', ''),
        }
        driver_data = {
            'license_number': data['license_number'],
            'phone': data.get('phone', ''),
        }
        try:
            driver = create_driver_with_user(user_data, driver_data)
            return Response(DriverSerializer(driver).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RegisterCustomerView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterCustomerSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = services.register_customer(serializer.validated_data)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'token': token.key,
            'username': token.user.email,
            'first_name': token.user.first_name,
            'is_superuser': False,
        }, status=status.HTTP_201_CREATED)


# ─── User Management (superadmin only) ───────────────────────

class UserListView(APIView):
    permission_classes = [IsSuperAdmin]

    def get(self, request):
        users = services.get_all_users()
        return Response(UserSerializer(users, many=True).data)

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = services.create_user(serializer.validated_data)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class UserDetailView(APIView):
    permission_classes = [IsSuperAdmin]

    def get_object(self, pk):
        try:
            return User.objects.prefetch_related('groups').get(pk=pk)
        except User.DoesNotExist:
            return None

    def patch(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response({'detail': 'No encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        updated = services.update_user(user, request.data)
        return Response(UserSerializer(updated).data)

    def delete(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response({'detail': 'No encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        if user == request.user:
            return Response({'detail': 'No puedes eliminar tu propio usuario.'}, status=status.HTTP_400_BAD_REQUEST)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AssignGroupView(APIView):
    permission_classes = [IsSuperAdmin]

    def post(self, request, pk):
        try:
            user = User.objects.prefetch_related('groups').get(pk=pk)
        except User.DoesNotExist:
            return Response({'detail': 'No encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        group_id = request.data.get('group_id')
        action = request.data.get('action', 'add')
        try:
            updated = services.assign_group(user, group_id, action)
            return Response(UserSerializer(updated).data)
        except Group.DoesNotExist:
            return Response({'detail': 'Grupo no encontrado.'}, status=status.HTTP_404_NOT_FOUND)


# ─── Group Management (superadmin only) ──────────────────────

class GroupListView(APIView):
    permission_classes = [IsSuperAdmin]

    def get(self, request):
        groups = services.get_all_groups()
        return Response(GroupSerializer(groups, many=True).data)

    def post(self, request):
        name = request.data.get('name', '').strip()
        if not name:
            return Response({'detail': 'Nombre requerido.'}, status=status.HTTP_400_BAD_REQUEST)
        group = services.create_group(name)
        return Response(GroupSerializer(group).data, status=status.HTTP_201_CREATED)


class GroupDetailView(APIView):
    permission_classes = [IsSuperAdmin]

    def delete(self, request, pk):
        services.delete_group(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        try:
            group = Group.objects.prefetch_related('permissions').get(pk=pk)
        except Group.DoesNotExist:
            return Response({'detail': 'No encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        permission_ids = request.data.get('permission_ids', [])
        group.permissions.set(Permission.objects.filter(id__in=permission_ids))
        return Response(GroupSerializer(group).data)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class PermissionListView(APIView):
    permission_classes = [IsSuperAdmin]

    def get(self, request):
        # solo permisos de las apps del proyecto
        apps = ['products', 'tables', 'reservations', 'shipments', 'warehouses',
                'suppliers', 'transport', 'drivers', 'routes', 'customers']
        perms = Permission.objects.filter(
            content_type__app_label__in=apps
        ).select_related('content_type').order_by('content_type__app_label', 'codename')
        return Response(PermissionSerializer(perms, many=True).data)
