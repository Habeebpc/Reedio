from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    ListCreateAPIView
)
from admin_panel.serializers import (
    CategorySerializer,
    SubCategorySerializer,
    PlayListSerializer,
    PodcastSerializer,
    AddPlayListToPodcastSerializer,
    DeletedPlayListSerializer,
    PackageSerializer,
    PodcastAnalyticsSerializer
)

from admin_panel.models import (
    Category,
    SubCategory,
    Podcast,
    PlayList,
    Package
)
from user_auth.permission import IsPartnerUser
from django_filters.rest_framework import DjangoFilterBackend
from podcast_app.response import SuccessResponse


class CategoryListView(ListAPIView):
    permission_classes = [IsPartnerUser]
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('-id')


class SubCategoryListView(ListAPIView):
    permission_classes = [IsPartnerUser]
    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all().order_by('-id')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', ]


class PackageListCreateView(ListAPIView):
    permission_classes = [IsPartnerUser]
    serializer_class = PackageSerializer
    queryset = Package.objects.all()
    filter_backends = [DjangoFilterBackend]


class PodcastListCreateView(ListCreateAPIView):
    permission_classes = [IsPartnerUser]
    serializer_class = PodcastSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_approved', 'category', 'sub_category']

    def get_queryset(self):
        return Podcast.objects.filter(
            created_by=self.request.user).order_by('-id')

    def get_serializer_context(self):
        return {'user': self.request.user}


class PodcastUpdateView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsPartnerUser]
    serializer_class = PodcastSerializer
    queryset = Podcast.objects.all()
    allowed_methods = ['GET', 'PATCH', 'DELETE']


class PlayListUpdateView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsPartnerUser]
    serializer_class = PlayListSerializer
    queryset = PlayList.objects.all()
    allowed_methods = ['GET', 'PATCH', 'DELETE']

    def delete(self, request, *args, **kwargs):
        playlist = self.get_object()
        playlist.is_trashed = True
        playlist.save()
        return SuccessResponse(message='Playlist deleted successfully')


class AddPlayListToPodcastView(ListCreateAPIView):
    permission_classes = [IsPartnerUser]
    serializer_class = AddPlayListToPodcastSerializer

    def get_queryset(self):
        return PlayList.objects.filter(
            podcast__id=self.kwargs.get('pk'),
            is_trashed=False
        ).order_by('-id')

    def get_serializer_context(self):
        return {'podcast_id': self.kwargs.get('pk')}


class DeletedPlayListView(ListAPIView):
    permission_classes = [IsPartnerUser]
    serializer_class = DeletedPlayListSerializer

    def get_queryset(self):
        if self.request.user.user_type == 2:
            return PlayList.objects.filter(
                podcast__created_by=self.request.user,
                is_trashed=True
            ).order_by('-id')
        return PlayList.objects.filter(is_trashed=True).order_by('-id')

    def get_serializer_context(self):
        return {'user': self.request.user}


class PodcastAnalyticsView(ListAPIView):
    permission_classes = [IsPartnerUser]
    serializer_class = PodcastAnalyticsSerializer

    def get_queryset(self):
        return Podcast.objects.filter(
            created_by=self.request.user).order_by('-id')
