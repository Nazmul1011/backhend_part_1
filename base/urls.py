from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import register_user, me_view, list_users, delete_user, logout_view

urlpatterns = [
    # Auth (JWT)
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", logout_view, name="logout"),

    # User management (FBVs)
    path("users/register/", register_user, name="users_register"),
    path("users/me/", me_view, name="users_me"),
    path("users/", list_users, name="users_list"),                
    path("users/<int:user_id>/", delete_user, name="users_delete"),
]
