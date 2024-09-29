from django.urls import path
from .views import (
    MyPartnersListView,
    MyPartnerPodcastListView,
    MyPartnerPodcastDetailView,
    AccessCodeGenerationView
)


urlpatterns = [
    path('partners/', MyPartnersListView.as_view()),
    path('partner-podcasts/', MyPartnerPodcastListView.as_view()),
    path('partner-podcast/<int:pk>/', MyPartnerPodcastDetailView.as_view()),
    path('access-codes/', AccessCodeGenerationView.as_view())
]
