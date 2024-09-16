from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    UpdateAPIView,
    CreateAPIView
)
from customer.serializers import (
    CategoryListSerializer,
    SubCategoryListSerializer,
    PodcastListSerializer,
    PodcastDetailSerializer,
    AddToFavoriteSerializer,
    AddToFavoriteAudioSerializer,
    AudioProgressSerializer,
    RedeemAccessCodeSerializer
)

from admin_panel.models import Category, SubCategory, Podcast
from customer.models import Favorite, FavoriteAudio, AudioProgress
from user_auth.permission import IsCustomerUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from podcast_app.response import SuccessResponse, ErrorResponse


class CategoryListView(ListAPIView):
    permission_classes = [IsCustomerUser]
    serializer_class = CategoryListSerializer
    queryset = Category.objects.all().order_by('-id')


class SubCategoryListView(ListAPIView):
    permission_classes = [IsCustomerUser]
    serializer_class = SubCategoryListSerializer
    queryset = SubCategory.objects.all().order_by('-id')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']


class PodCastListView(ListAPIView):
    permission_classes = [IsCustomerUser]
    serializer_class = PodcastListSerializer
    queryset = Podcast.objects.filter(is_approved=True).order_by('-id')
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category', 'sub_category']
    search_fields = ['name', 'description']

    def get_serializer_context(self):
        return {'user': self.request.user}


class PodCastDetailView(RetrieveAPIView):
    permission_classes = [IsCustomerUser]
    serializer_class = PodcastDetailSerializer
    queryset = Podcast.objects.filter(is_approved=True).order_by('-id')

    def get_serializer_context(self):
        return {'user': self.request.user}


class FavoriteListCreateView(ListCreateAPIView):
    permission_classes = [IsCustomerUser]
    serializer_class = AddToFavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class FavoriteRemoveView(DestroyAPIView):
    permission_classes = [IsCustomerUser]
    serializer_class = AddToFavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).order_by('-id')


class FavoriteAudioListCreateView(ListCreateAPIView):
    permission_classes = [IsCustomerUser]
    serializer_class = AddToFavoriteAudioSerializer

    def get_queryset(self):
        return FavoriteAudio.objects.filter(
            user=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class FavoriteAudioRemoveView(DestroyAPIView):
    permission_classes = [IsCustomerUser]
    serializer_class = AddToFavoriteAudioSerializer

    def get_queryset(self):
        return FavoriteAudio.objects.filter(
            user=self.request.user).order_by('-id')


class AudioProgressApiView(UpdateAPIView):
    permission_classes = [IsCustomerUser]
    serializer_class = AudioProgressSerializer
    allowed_methods = ['PUT']

    def get_object(self):
        return AudioProgress.objects.filter(
            user=self.request.user,
            audio__id=self.kwargs.get('pk')
        ).first()


class RedeemAccessCodeView(CreateAPIView):
    permission_classes = [IsCustomerUser]
    serializer_class = RedeemAccessCodeSerializer

    def post(self, request):
        serializer = RedeemAccessCodeSerializer(
            context={'user': self.request.user}, data=request.data)
        if serializer.is_valid():
            return SuccessResponse(data=serializer.validated_data)
        error = 'Error'
        if serializer.errors.get('non_field_errors'):
            error = serializer.errors["non_field_errors"][0]
        return ErrorResponse(message=error)
