from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    ListCreateAPIView,
    UpdateAPIView
)
from retailer.serializers import (
    MyPartnersSerializer,
    MyPartnerPodcastListSerializer,
    MyPartnerPodcastDetailSerializer,
    AccessCodeGenerationSerializer,
    AccessCodeSentSerializer
)
from user_auth.permission import IsRetailerUser
from user_auth.models import PartnerAndRetailer
from admin_panel.models import Podcast
from retailer.models import AccessCode
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


class MyPartnersListView(ListAPIView):
    permission_classes = [IsRetailerUser]
    serializer_class = MyPartnersSerializer
    filter_backends = [SearchFilter]
    search_fields = ['partner__name']

    def get_queryset(self):
        return PartnerAndRetailer.objects.filter(
            retailer=self.request.user,
            is_active=True
        ).order_by('partner__name')


class MyPartnerPodcastListView(ListAPIView):
    permission_classes = [IsRetailerUser]
    serializer_class = MyPartnerPodcastListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name', 'description']
    filterset_fields = ['created_by',]

    def get_queryset(self):
        partners = PartnerAndRetailer.objects.filter(
            retailer=self.request.user,
            is_active=True
        ).values_list('partner', flat=True)
        return Podcast.objects.filter(
            created_by__in=partners,
            is_approved=True
        ).order_by('-id')


class MyPartnerPodcastDetailView(RetrieveAPIView):
    permission_classes = [IsRetailerUser]
    serializer_class = MyPartnerPodcastDetailSerializer
    queryset = Podcast.objects.filter(is_approved=True)


class AccessCodeGenerationView(ListCreateAPIView):
    permission_classes = [IsRetailerUser]
    serializer_class = AccessCodeGenerationSerializer

    def get_queryset(self):
        return AccessCode.objects.filter(created_by=self.request.user)

    def get_serializer_context(self):
        return {'user': self.request.user}


class AccessCodeSentView(UpdateAPIView):
    permission_classes = [IsRetailerUser]
    serializer_class = AccessCodeSentSerializer
    queryset = AccessCode.objects.filter(sent_to__isnull=True)
    allowed_methods = ['PUT']
