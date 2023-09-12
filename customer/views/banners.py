from rest_framework.generics import ListAPIView, RetrieveAPIView
from customer.serializers import (
    MainBannerSerializer,
    SubBannerSerializer,
    AppSettingsSerializer
)

from admin_panel.models import Banner, DummyImage, Settings
from user_auth.permission import IsCustomerUser


class MainBannerListView(ListAPIView):
    permission_classes = [IsCustomerUser]
    serializer_class = MainBannerSerializer
    queryset = Banner.objects.all().order_by('-id')


class SubBannerListView(ListAPIView):
    permission_classes = [IsCustomerUser]
    serializer_class = SubBannerSerializer
    queryset = DummyImage.objects.all().order_by('-id')


class SettingsApiView(RetrieveAPIView):
    permission_classes = [IsCustomerUser]
    serializer_class = AppSettingsSerializer
    queryset = Settings.objects.all()

    def get_object(self):
        return Settings.objects.last()
