from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from admin_panel.serializers import CustomersListSerializer, QuarriesSerializer
from user_auth.permission import IsAdminOrSubAdminUser
from user_auth.models import User
from customer.models import HelpDesk
from django_filters.rest_framework import DjangoFilterBackend


class CustomersListView(ListAPIView):
    permission_classes = (IsAdminOrSubAdminUser,)
    serializer_class = CustomersListSerializer
    queryset = User.objects.filter(user_type=3).order_by('-id')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['premium_user', ]


class QuarriesListView(ListAPIView):
    permission_classes = [IsAdminOrSubAdminUser]
    serializer_class = QuarriesSerializer
    queryset = HelpDesk.objects.all().order_by('-id')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_replied']


class QuarriesDetailView(RetrieveUpdateAPIView):
    permission_classes = [IsAdminOrSubAdminUser]
    serializer_class = QuarriesSerializer
    queryset = HelpDesk.objects.all()
    allowed_methods = ['GET', 'PATCH']
