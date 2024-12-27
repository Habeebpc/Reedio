from django.urls import path
from partner.views import (
    CategoryListView,
    SubCategoryListView,
    PackageListCreateView,
    PodcastListCreateView,
    PodcastUpdateView,
    PlayListUpdateView,
    AddPlayListToPodcastView,
    DeletedPlayListView,
    RetailerListCreateView,
    RetailerStatusUpdateSerializer,
    AccessCodeEnrolledView,
    PodcastAnalyticsView,
    PodcastPurchaseDetailView

)

urlpatterns = [
    # podcast
    path('categories/', CategoryListView.as_view()),
    path('sub-categories/', SubCategoryListView.as_view()),
    path('packages/', PackageListCreateView.as_view()),
    path('podcasts/', PodcastListCreateView.as_view()),
    path('podcast/<int:pk>/', PodcastUpdateView.as_view()),
    path('podcast/<int:pk>/playlists/', AddPlayListToPodcastView.as_view()),
    path('playlist/<int:pk>/', PlayListUpdateView.as_view()),
    path('deleted-playlists/', DeletedPlayListView.as_view()),
    path('retailers/', RetailerListCreateView.as_view()),
    path('retailer/<int:pk>/', RetailerStatusUpdateSerializer.as_view()),
    path('access-codes/', AccessCodeEnrolledView.as_view()),
    path('podcast/analytics/', PodcastAnalyticsView.as_view()),
    path('podcast/<int:pk>/purchase-detail/',
         PodcastPurchaseDetailView.as_view()),
]
