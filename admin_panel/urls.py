from django.urls import path
from admin_panel.views import (
    SubAdminListCreateView,
    SubAdminUpdateView,
    CategoryListCreateView,
    CategoryUpdateView,
    SubCategoryListCreateView,
    SubCategoryUpdateView,
    PodcastListCreateView,
    PodcastUpdateView,
    PodcastAdminApprovalView,
    PlayListUpdateView,
    CustomersListView,
    BannerListCreateView,
    BannerUpdateView,
    DummyImageListCreateView,
    DummyImageUpdateView,
    QuarriesListView,
    QuarriesDetailView
)

urlpatterns = [
    # sub admin
    path('sub-admins/', SubAdminListCreateView.as_view()),
    path('sub-admin/<int:pk>/', SubAdminUpdateView.as_view()),

    # podcast
    path('categories/', CategoryListCreateView.as_view()),
    path('category/<int:pk>/', CategoryUpdateView.as_view()),
    path('sub-categories/', SubCategoryListCreateView.as_view()),
    path('sub-category/<int:pk>/', SubCategoryUpdateView.as_view()),
    path('podcasts/', PodcastListCreateView.as_view()),
    path('podcast/<int:pk>/', PodcastUpdateView.as_view()),
    path('podcast/<int:pk>/approve/', PodcastAdminApprovalView.as_view()),
    path('playlist/<int:pk>/', PlayListUpdateView.as_view()),

    # customer
    path('customers/', CustomersListView.as_view()),

    # banners
    path('main-banners/', BannerListCreateView.as_view()),
    path('main-banner/<int:pk>/', BannerUpdateView.as_view()),
    path('sub-banners/', DummyImageListCreateView.as_view()),
    path('sub-banner/<int:pk>/', DummyImageUpdateView.as_view()),

    # Quarries
    path('quarries/', QuarriesListView.as_view()),
    path('quarries/<int:pk>/', QuarriesDetailView.as_view())
]
