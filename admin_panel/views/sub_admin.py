from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from admin_panel.serializers import (
    SubAdminListCreateSerializer,
    PartnerListCreateSerializer
)
from user_auth.models import User
from user_auth.permission import IsAdminUser


class SubAdminListCreateView(ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = SubAdminListCreateSerializer
    queryset = User.objects.filter(user_type=2).order_by('-id')


class SubAdminUpdateView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = SubAdminListCreateSerializer
    queryset = User.objects.filter(user_type=2)
    allowed_methods = ['GET', 'PATCH', 'DELETE']


class PartnerListCreateView(ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = PartnerListCreateSerializer
    queryset = User.objects.filter(user_type=4).order_by('-id')


class PartnerUpdateView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = PartnerListCreateSerializer
    queryset = User.objects.filter(user_type=4)
    allowed_methods = ['GET', 'PATCH', 'DELETE']
