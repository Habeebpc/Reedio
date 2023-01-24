from django.urls import path

from plot.views import (
    PlotListCreateView,
    PlotRetrieveUpdateDestroyView,
    MeetingListCreateView,
    MeetingRetrieveUpdateDestroyView,
    TransactionCategoryListCreateView,
    TransactionCategoryRetrieveUpdateDestroyView,
    TransactionListCreateView,
    TransactionRetrieveUpdateDestroyView,
)
urlpatterns = [
    path('plots/', PlotListCreateView.as_view(), name='plot-list-create'),
    path('plots/<int:pk>/', PlotRetrieveUpdateDestroyView.as_view(),
         name='plot-retrieve-update-destroy'),
    path('meetings/', MeetingListCreateView.as_view(), name='meeting-list-create'),
    path('meetings/<int:pk>/', MeetingRetrieveUpdateDestroyView.as_view(),
         name='meeting-retrieve-update-destroy'),
    path('transaction-categories/', TransactionCategoryListCreateView.as_view(),
         name='transaction-category-list-create'),
    path('transaction-categories/<int:pk>/', TransactionCategoryRetrieveUpdateDestroyView.as_view(),
         name='transaction-category-retrieve-update-destroy'),
    path('transactions/', TransactionListCreateView.as_view(),
         name='transaction-list-create'),
    path('transactions/<int:pk>/', TransactionRetrieveUpdateDestroyView.as_view(),
         name='transaction-retrieve-update-destroy'),
]
