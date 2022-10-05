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



error_logger = logging.getLogger('error_logger')


class UserJWTSerializer(TokenObtainPairSerializer):
    ''' Custom JWT claim '''
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.name
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = text_type(refresh)
        data['access'] = text_type(refresh.access_token)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'name',  'username', 'password', 'profile_photo')
        read_only_fields = ('id', 'username',)
        extra_kwargs = {'password': {'write_only': True, 'required': True},
                        'name': {'required': True}, }

    def create(self, validated_data):
        validated_data['email'] = validated_data['email'].lower()
        validated_data['username'] = validated_data['mobile']
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if validated_data.get('password'):
            password = validated_data.pop('password')
            instance.set_password(password)
        instance = super(UserSerializer, self).update(instance, validated_data)
        return instance


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
