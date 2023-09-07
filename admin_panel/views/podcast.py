from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView
)
from admin_panel.serializers import (
    CategorySerializer,
    SubCategorySerializer,
    PlayListSerializer,
    PodcastSerializer,
    PodcastAdminApprovalSerializer,
    AddPlayListToPodcastSerializer
)

from admin_panel.models import Category, SubCategory, Podcast, PlayList
from user_auth.permission import IsAdminOrSubAdminUser, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend


class CategoryListCreateView(ListCreateAPIView):
    permission_classes = [IsAdminOrSubAdminUser]
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('-id')


class CategoryUpdateView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrSubAdminUser]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    allowed_methods = ['GET', 'PATCH', 'DELETE']


class SubCategoryListCreateView(ListCreateAPIView):
    permission_classes = [IsAdminOrSubAdminUser]
    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all().order_by('-id')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', ]


class SubCategoryUpdateView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrSubAdminUser]
    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all()
    allowed_methods = ['GET', 'PATCH', 'DELETE']


class PodcastListCreateView(ListCreateAPIView):
    permission_classes = [IsAdminOrSubAdminUser]
    serializer_class = PodcastSerializer
    queryset = Podcast.objects.all().order_by('-id')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_approved', 'category', 'sub_category']


class PodcastUpdateView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrSubAdminUser]
    serializer_class = PodcastSerializer
    queryset = Podcast.objects.all()
    allowed_methods = ['GET', 'PATCH', 'DELETE']


class PlayListUpdateView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrSubAdminUser]
    serializer_class = PlayListSerializer
    queryset = PlayList.objects.all()
    allowed_methods = ['GET', 'PATCH', 'DELETE']


class PodcastAdminApprovalView(UpdateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = PodcastAdminApprovalSerializer
    queryset = Podcast.objects.all()
    allowed_methods = ['PUT', ]


class AddPlayListToPodcastView(ListCreateAPIView):
    permission_classes = [IsAdminOrSubAdminUser]
    serializer_class = AddPlayListToPodcastSerializer

    def get_queryset(self):
        return PlayList.objects.filter(podcast__id=self.kwargs.get('pk'))

    def get_serializer_context(self):
        return {'podcast_id': self.kwargs.get('pk')}
