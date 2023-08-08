from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from django.conf import settings
import jwt


class IsAuthenticatedUser(IsAuthenticated):
    def has_permission(self, request, view):
        if not request.user.is_anonymous and \
            not request.user.is_blocked_user and \
                super(IsAuthenticatedUser, self).has_permission(request, view):

            jwt_secret = settings.SIMPLE_JWT.get('SIGNING_KEY')
            token = request.META.get("HTTP_AUTHORIZATION").split()[1]
            jti = jwt.decode(token, jwt_secret,
                             algorithms=["HS256"])['jti']
            if cache.get(jti):
                return True
            return False

        return False


class IsAdminUser(IsAuthenticated):
    def has_permission(self, request, view):
        if not request.user.is_anonymous and \
            request.user.user_type == 1 and \
                super(IsAdminUser, self).has_permission(request, view):

            jwt_secret = settings.SIMPLE_JWT.get('SIGNING_KEY')
            token = request.META.get("HTTP_AUTHORIZATION").split()[1]
            jti = jwt.decode(token, jwt_secret,
                             algorithms=["HS256"])['jti']
            if cache.get(jti):
                return True
            return False

        return False


class IsAdminOrSubAdminUser(IsAuthenticated):
    def has_permission(self, request, view):
        if not request.user.is_anonymous and \
            request.user.user_type in [1, 2] and \
                super(IsAdminOrSubAdminUser, self).has_permission(request, view):

            jwt_secret = settings.SIMPLE_JWT.get('SIGNING_KEY')
            token = request.META.get("HTTP_AUTHORIZATION").split()[1]
            jti = jwt.decode(token, jwt_secret,
                             algorithms=["HS256"])['jti']
            if cache.get(jti):
                return True
            return False
        return False


class IsCustomerUser(IsAuthenticated):
    def has_permission(self, request, view):
        if not request.user.is_anonymous and \
            request.user.user_type == 3 and \
                super(IsCustomerUser, self).has_permission(request, view):

            jwt_secret = settings.SIMPLE_JWT.get('SIGNING_KEY')
            token = request.META.get("HTTP_AUTHORIZATION").split()[1]
            jti = jwt.decode(token, jwt_secret,
                             algorithms=["HS256"])['jti']
            if cache.get(jti):
                return True
            return False
        return False


class IsPremiumCustomerUser(IsAuthenticated):
    def has_permission(self, request, view):
        if not request.user.is_anonymous and \
            request.user.user_type == 3 and \
            request.user.premium_user and \
                super(IsPremiumCustomerUser, self).has_permission(request, view):

            jwt_secret = settings.SIMPLE_JWT.get('SIGNING_KEY')
            token = request.META.get("HTTP_AUTHORIZATION").split()[1]
            jti = jwt.decode(token, jwt_secret,
                             algorithms=["HS256"])['jti']
            if cache.get(jti):
                return True
            return False
        return False
