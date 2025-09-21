from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer, RegisterSerializer

User = get_user_model()

def _is_admin(user):
    return getattr(user, "role", "") == "ADMIN" or user.is_superuser


@api_view(["POST"])
@permission_classes([AllowAny])  
def register_user(request):
   
    
    data = request.data.copy()
    if not (request.user and request.user.is_authenticated and _is_admin(request.user)):
        
        data["role"] = "ADMIN"

    serializer = RegisterSerializer(data=data, context={"request": request})
    if serializer.is_valid():
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me_view(request):
    return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_users(request):
   
    if _is_admin(request.user):
        qs = User.objects.all().order_by("id")
    else:
        qs = User.objects.filter(id=request.user.id)
    return Response(UserSerializer(qs, many=True).data, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_user(request, user_id: int):
    
    if not _is_admin(request.user):
        return Response({"detail": "Admins only."}, status=status.HTTP_403_FORBIDDEN)

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    if user.is_superuser:
        return Response({"detail": "Cannot delete superuser."}, status=status.HTTP_400_BAD_REQUEST)

    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
   
    refresh = request.data.get("refresh")
    if not refresh:
        return Response({"detail": "Refresh token required."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        token = RefreshToken(refresh)
        token.blacklist()
    except Exception:
        return Response({"detail": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"detail": "Logged out."}, status=status.HTTP_205_RESET_CONTENT)
