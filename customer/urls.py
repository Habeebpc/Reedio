from django.urls import path
from customer.views import (
    MainBannerListView,
    SubBannerListView,
    CategoryListView,
    SubCategoryListView,
    PodCastListView,
    PodCastDetailView,
    FavoriteListCreateView,
    FavoriteRemoveView,
    ProfileView,
    UpgradeToPremium,
    HelpDeskView,
    HelpDeskEditView,
    SettingsApiView,
    FavoriteAudioListCreateView,
    FavoriteAudioRemoveView,
    AudioProgressApiView,
    RedeemAccessCodeView
)

urlpatterns = [
    path('main-banners/', MainBannerListView.as_view()),
    path('sub-banners/', SubBannerListView.as_view()),
    path('categories/', CategoryListView.as_view()),
    path('sub-categories/', SubCategoryListView.as_view()),
    path('podcasts/', PodCastListView.as_view()),
    path('podcast/<int:pk>/detail', PodCastDetailView.as_view()),
    path('favorites/', FavoriteListCreateView.as_view()),
    path('favorite/<int:pk>/remove', FavoriteRemoveView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('upgrade-to-premium', UpgradeToPremium.as_view()),
    path('quarries/', HelpDeskView.as_view()),
    path('quarries/<int:pk>/', HelpDeskEditView.as_view()),
    path('settings/', SettingsApiView.as_view()),
    path('favorite-audios/', FavoriteAudioListCreateView.as_view()),
    path('favorite-audio/<int:pk>/remove', FavoriteAudioRemoveView.as_view()),
    path('audio/<int:pk>/progress/', AudioProgressApiView.as_view()),
    path('redeem-access-code/', RedeemAccessCodeView.as_view())
]
