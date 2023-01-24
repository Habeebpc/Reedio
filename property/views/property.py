from property.models import Property

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from user_auth.permission import IsAuthenticatedUser

from property.serializers import (
    PropertyListSerializer,
    PropertyCreateSerializer
)


class PropertyListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticatedUser,)
    queryset = Property.objects.all()

    def get_serializer_context(self):
        return {'user': self.request.user}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PropertyCreateSerializer
        return PropertyListSerializer


class PropertyRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedUser,)
    queryset = Property.objects.all()
    serializer_class = PropertyCreateSerializer
