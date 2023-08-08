from rest_framework.generics import ListAPIView
from customer.serializers import (
    MainBannerSerializer,
    SubBannerSerializer
)

from admin_panel.models import Banner, DummyImage
from user_auth.permission import IsCustomerUser


class MainBannerListView(ListAPIView):
    permission_classes = [IsCustomerUser]
    serializer_class = MainBannerSerializer
    queryset = Banner.objects.all().order_by('-id')


class SubBannerListView(ListAPIView):
    permission_classes = [IsCustomerUser]
    serializer_class = SubBannerSerializer
    queryset = DummyImage.objects.all().order_by('-id')
