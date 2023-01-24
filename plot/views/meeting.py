from plot.models import Meeting

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from user_auth.permission import IsAuthenticatedUser

from plot.serializers import (
    MeetingCreateSerializer,
    MeetingListSerializer
)


class MeetingListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticatedUser,)
    queryset = Meeting.objects.all()

    def get_serializer_context(self):
        return {'user': self.request.user}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MeetingCreateSerializer
        return MeetingListSerializer


class MeetingRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedUser,)
    queryset = Meeting.objects.all()
    serializer_class = MeetingCreateSerializer
