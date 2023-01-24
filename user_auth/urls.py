from django.urls import path
from user_auth.views import (
    LoginView,
    PasswordResetView,
    LogoutView,
    TokenRefreshView,
    UsersListCreateView,
    UserRetrieveUpdateDestroyView,
)
from rest_framework_simplejwt.views import TokenVerifyView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login-view'),
    path('refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('password/reset/', PasswordResetView.as_view(),
         name='reset-password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('users/', UsersListCreateView.as_view(), name='users-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(),
         name='user-retrieve-update-destroy'),
]
