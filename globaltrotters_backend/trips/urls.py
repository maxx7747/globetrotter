from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TripViewSet

router = DefaultRouter()
router.register(r'', TripViewSet, basename='trip')

urlpatterns = [
    path('', include(router.urls)),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TripViewSet, TripActivityListCreateView

router = DefaultRouter()
router.register(r'', TripViewSet, basename='trip')

urlpatterns = [
    path('', include(router.urls)),
    # Nested route for fetching/creating activities bound to a trip
    path('<int:trip_pk>/activities/', TripActivityListCreateView.as_view(), name='trip-activities'),
]