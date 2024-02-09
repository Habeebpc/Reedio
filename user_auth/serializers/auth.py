from django.conf import settings
from six import text_type
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import logging
from rest_framework import serializers
from django.contrib.auth import authenticate
from user_auth.models import User
from django.core.cache import cache
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
import jwt
from decouple import config
import string
import random
from django.shortcuts import get_object_or_404

error_logger = logging.getLogger('error_logger')


def generate_number(length):
    digits = string.digits
    numbers = ''.join(random.choice(digits) for i in range(length))
    return numbers


class UserJWTSerializer(TokenObtainPairSerializer):
    ''' Custom JWT claim '''
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.name
        token['premium_user'] = user.premium_user
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = text_type(refresh)
        data['access'] = text_type(refresh.access_token)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'name', 'mobile',
                  'email', 'user_type', 'premium_user')


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(max_length=128, write_only=True,
                                     required=False)

    def validate(self, attrs):
        user = None
        credentials = {
            'username': attrs.get('username').lower(),
            'password': attrs.get('password')
        }

        if not all(credentials.values()):
            message = 'Must include username and password'
            raise serializers.ValidationError(message)
        user = None
        try:
            user = authenticate(**credentials)
        except Exception as e:
            error_logger.info(e)
        data = {}
        if not user:
            message = 'Invalid Credentials'
            raise serializers.ValidationError(message)
        token = UserJWTSerializer.get_token(user)
        acc = token.access_token
        cache.set(acc['jti'], user.id, timeout=1728000)

        auth = {
            'refresh': str(token),
            'access': str(acc),
        }
        user_serializer = UserSerializer(user)
        data = {'token': auth, 'user': user_serializer.data}
        return data


class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        password = attrs.get('password')
        user = self.context.get('user')
        user.set_password(password)
        user.save()
        return user


class CustomTokenRefreshSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        access_token = data['access']
        jwt_secret = settings.SIMPLE_JWT.get('SIGNING_KEY')
        jti = jwt.decode(access_token, jwt_secret,
                         algorithms=["HS256"])['jti']
        cache.set(jti, timeout=1728000)
        return data


class GoogleLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    token = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        token = attrs.get('token')

        user = get_object_or_404(User, email=email)

        if token != config('SECURITY_TOKEN'):
            raise serializers.ValidationError('oops, something went wrong')

        if user.user_type != 3:
            raise serializers.ValidationError('you have no permission')

        credentials = {
            'username': user.username,
            'password': config('SOCIAL_AUTH_PASSWORD')
        }
        user = authenticate(**credentials)

        token = UserJWTSerializer.get_token(user)
        acc = token.access_token
        cache.set(acc['jti'], user.id, timeout=1728000)
        auth = {
            'refresh': str(token),
            'access': str(acc),
        }
        user_serializer = UserSerializer(user)
        data = {'token': auth, 'user': user_serializer.data}
        return data


class UserRegistrationSerializer(serializers.Serializer):
    name = serializers.CharField()
    mobile = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    token = serializers.CharField(required=True)

    def validate(self, attrs):
        name = attrs.get('name')
        mobile = attrs.get('mobile')
        email = attrs.get('email')
        token = attrs.get('token')

        if token != config('SECURITY_TOKEN'):
            raise serializers.ValidationError('oops, something went wrong')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'user with this email already exists')
        if User.objects.filter(mobile=mobile).exists():
            raise serializers.ValidationError(
                'user with this mobile number already exists')

        username = email.split('@')[0]+generate_number(5)
        password = config('SOCIAL_AUTH_PASSWORD')
        User.objects.create_user(
            email=email,
            name=name,
            mobile=mobile,
            username=username,
            password=password,
            user_type=3
        )
        user = authenticate(username=username, password=password)
        token = UserJWTSerializer.get_token(user)
        acc = token.access_token
        cache.set(acc['jti'], user.id, timeout=1728000)
        auth = {
            'refresh': str(token),
            'access': str(acc),
        }
        user_serializer = UserSerializer(user)
        data = {'token': auth, 'user': user_serializer.data}
        return data
