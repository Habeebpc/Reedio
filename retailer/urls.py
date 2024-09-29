from django.urls import path
from .views import (
    MyPartnersListView,
    MyPartnerPodcastListView,
    MyPartnerPodcastDetailView,
    AccessCodeGenerationView,
    AccessCodeSentView
)


urlpatterns = [
    path('partners/', MyPartnersListView.as_view()),
    path('partner-podcasts/', MyPartnerPodcastListView.as_view()),
    path('partner-podcast/<int:pk>/', MyPartnerPodcastDetailView.as_view()),
    path('access-codes/', AccessCodeGenerationView.as_view()),
    path('access-codes/<int:pk>/sent/', AccessCodeSentView.as_view()),
]
