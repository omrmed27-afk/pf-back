from django.urls import path
from .views import (
    LoginView, LogoutView, RegisterDriverView, RegisterCustomerView,
    UserListView, UserDetailView, AssignGroupView,
    GroupListView, GroupDetailView, PermissionListView, MeView,
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='auth-login'),
    path('logout/', LogoutView.as_view(), name='auth-logout'),
    path('register/', RegisterDriverView.as_view(), name='auth-register'),
    path('register-customer/', RegisterCustomerView.as_view(), name='auth-register-customer'),
    path('users/', UserListView.as_view(), name='auth-users'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='auth-user-detail'),
    path('users/<int:pk>/assign-group/', AssignGroupView.as_view(), name='auth-assign-group'),
    path('groups/', GroupListView.as_view(), name='auth-groups'),
    path('groups/<int:pk>/', GroupDetailView.as_view(), name='auth-group-detail'),
    path('permissions/', PermissionListView.as_view(), name='auth-permissions'),
    path('me/', MeView.as_view(), name='auth-me'),
]
