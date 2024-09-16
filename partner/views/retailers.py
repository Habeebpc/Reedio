from rest_framework.generics import (
    UpdateAPIView,
    ListAPIView,
    ListCreateAPIView
)
from partner.serializers import (
    RetailerSerializer,
    RetailerStatusUpdateSerializer,
    AccessCodeEnrolledSerializer
)
from user_auth.models import PartnerAndRetailer
from retailer.models import AccessCode

from user_auth.permission import IsPartnerUser
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class RetailerListCreateView(ListCreateAPIView):
    permission_classes = [IsPartnerUser]
    serializer_class = RetailerSerializer

    def get_queryset(self):
        return PartnerAndRetailer.objects.filter(
            partner=self.request.user,
        ).order_by('-id')

    def get_serializer_context(self):
        return {'user': self.request.user}


class RetailerStatusUpdateSerializer(UpdateAPIView):
    permission_classes = [IsPartnerUser]
    serializer_class = RetailerStatusUpdateSerializer
    queryset = PartnerAndRetailer.objects.all()
    allowed_methods = ['PUT']


class AccessCodeEnrolledView(ListAPIView):
    permission_classes = [IsPartnerUser]
    serializer_class = AccessCodeEnrolledSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['podcast', 'created_by']

    def get_queryset(self):
        return AccessCode.objects.filter(
            podcast__created_by=self.request.user
        )

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            'podcast', openapi.IN_QUERY,
            description="Filter by podcast",
            type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter(
            'created_by', openapi.IN_QUERY,
            description="Filter by creator",
            type=openapi.TYPE_INTEGER
        )
    ])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
