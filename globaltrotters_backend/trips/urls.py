from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TripViewSet, TripActivityListCreateView, TripExpenseListCreateView,
    CommunityTripListView, TripCloneView, CollaboratorListCreateView
)

router = DefaultRouter()
router.register(r'', TripViewSet, basename='trip')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:trip_pk>/activities/', TripActivityListCreateView.as_view(), name='trip-activities'),
    path('<int:trip_pk>/expenses/', TripExpenseListCreateView.as_view(), name='trip-expenses'),
    path('<int:trip_pk>/collaborators/', CollaboratorListCreateView.as_view(), name='trip-collaborators'),
]