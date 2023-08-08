from rest_framework.generics import (
    RetrieveAPIView,
    UpdateAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from customer.serializers import (
    ProfileSerializer,
    UpgradeToPremiumSerializer,
    HelpDeskSerializer
)
from user_auth.permission import IsCustomerUser, IsPremiumCustomerUser
from customer.models import HelpDesk


class ProfileView(RetrieveAPIView):
    permission_classes = [IsCustomerUser]
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user


class UpgradeToPremium(UpdateAPIView):
    permission_classes = [IsCustomerUser]
    serializer_class = UpgradeToPremiumSerializer
    allowed_methods = ['PUT']

    def get_object(self):
        return self.request.user


class HelpDeskView(ListCreateAPIView):
    permission_classes = [IsPremiumCustomerUser]
    serializer_class = HelpDeskSerializer

    def get_queryset(self):
        return HelpDesk.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class HelpDeskEditView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsPremiumCustomerUser]
    serializer_class = HelpDeskSerializer
    allowed_methods = ['GET', 'PATCH', 'DELETE']

    def get_queryset(self):
        return HelpDesk.objects.filter(user=self.request.user)
