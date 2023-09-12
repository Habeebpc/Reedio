from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    DestroyAPIView
)
from customer.serializers import (
    CategoryListSerializer,
    SubCategoryListSerializer,
    PodcastListSerializer,
    PodcastDetailSerializer,
    AddToFavoriteSerializer
)

from admin_panel.models import Category, SubCategory, Podcast
from customer.models import Favorite
from user_auth.permission import IsCustomerUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


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


class PodCastDetailView(RetrieveAPIView):
    permission_classes = [IsCustomerUser]
    serializer_class = PodcastDetailSerializer
    queryset = Podcast.objects.filter(is_approved=True).order_by('-id')


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
