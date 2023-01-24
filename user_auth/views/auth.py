from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.views import APIView
from user_auth.permission import IsAuthenticatedUser
from tech_plotz.response import (
    SuccessResponse,
    ErrorResponse
)
from user_auth.serializers import (
    AuthSerializer,
    UserPasswordResetSerializer,
    CustomTokenRefreshSerializer,
    UserCreateSerializer,
    UserUpdateSerializer
)
from django.core.cache import cache
from django.conf import settings
import jwt
from user_auth.models import User


class LoginView(CreateAPIView):
    serializer_class = AuthSerializer

    def post(self, request):

        token_serializer = AuthSerializer(data=request.data)
        if token_serializer.is_valid():
            return SuccessResponse(data=token_serializer.validated_data,
                                   message="Login successful")

        message = "Error"
        if token_serializer.errors.get('non_field_errors'):
            message = token_serializer.errors["non_field_errors"][0]
        return ErrorResponse(message=message)


class LogoutView(APIView):
    permission_classes = (IsAuthenticatedUser,)

    def post(self, request):
        token = request.META.get("HTTP_AUTHORIZATION").split()[1]
        jwt_secret = settings.SIMPLE_JWT.get('SIGNING_KEY')
        jti = jwt.decode(token, jwt_secret,
                         algorithms=["HS256"])['jti']
        cache.delete(jti)

        return SuccessResponse(message="Successfully logged out")


class PasswordResetView(CreateAPIView):
    permission_classes = (IsAuthenticatedUser, )
    serializer_class = UserPasswordResetSerializer

    def post(self, request):
        data = request.data
        context = {'user': request.user}
        reset_serializer = self.get_serializer(data=data, context=context)
        if reset_serializer.is_valid():
            token = request.META.get("HTTP_AUTHORIZATION").split()[1]
            jwt_secret = settings.SIMPLE_JWT.get('SIGNING_KEY')
            token = request.META.get("HTTP_AUTHORIZATION").split()[1]
            jti = jwt.decode(token, jwt_secret,
                             algorithms=["HS256"])['jti']
            cache.delete(jti)
            message = "Password reset successful. Login with the new \
                credentials to continue."
            return SuccessResponse(message=message)

        message = "Password reset failed"
        if reset_serializer.errors.get('non_field_errors'):
            message = reset_serializer.errors["non_field_errors"][0]
        return ErrorResponse(message=message)


class TokenRefreshView(CreateAPIView):
    serializer_class = CustomTokenRefreshSerializer

    def post(self, request):
        serializer = CustomTokenRefreshSerializer(data=request.data)
        if serializer.is_valid():
            return SuccessResponse(data=serializer.validated_data,
                                   message="Login successful")

        return ErrorResponse(message="Error")


class UsersListCreateView(ListCreateAPIView):
    # permission_classes = (IsAuthenticatedUser, )
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedUser, )
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message="User deleted successfully")
