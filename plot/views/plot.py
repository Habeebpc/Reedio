from plot.models import Plot

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from user_auth.permission import IsAuthenticatedUser

from plot.serializers import (
    PlotListSerializer,
    PlotCreateSerializer
)


class PlotListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticatedUser,)
    queryset = Plot.objects.all()

    def get_serializer_context(self):
        return {'user': self.request.user}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PlotCreateSerializer
        return PlotListSerializer


class PlotRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedUser,)
    queryset = Plot.objects.all()
    serializer_class = PlotCreateSerializer
