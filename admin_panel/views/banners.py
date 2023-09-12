from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveUpdateAPIView
)
from admin_panel.serializers import (
    BannerSerializer,
    DummyImageSerializer,
    SettingsSerializer
)

from admin_panel.models import Banner, DummyImage, Settings
from user_auth.permission import IsAdminOrSubAdminUser


class BannerListCreateView(ListCreateAPIView):
    permission_classes = [IsAdminOrSubAdminUser]
    serializer_class = BannerSerializer
    queryset = Banner.objects.all().order_by('-id')


class BannerUpdateView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrSubAdminUser]
    serializer_class = BannerSerializer
    queryset = Banner.objects.all()
    allowed_methods = ['GET', 'PATCH', 'DELETE']


class DummyImageListCreateView(ListCreateAPIView):
    permission_classes = [IsAdminOrSubAdminUser]
    serializer_class = DummyImageSerializer
    queryset = DummyImage.objects.all().order_by('-id')


class DummyImageUpdateView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrSubAdminUser]
    serializer_class = DummyImageSerializer
    queryset = DummyImage.objects.all()
    allowed_methods = ['GET', 'PATCH', 'DELETE']


class SettingsUpdateView(RetrieveUpdateAPIView):
    permission_classes = [IsAdminOrSubAdminUser]
    serializer_class = SettingsSerializer
    allowed_methods = ['GET', 'PUT']

    def get_object(self):
        return Settings.objects.last()
