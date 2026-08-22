

# Create your views here.
from rest_framework import viewsets
from .models import Trip
from .serializers import TripSerializer
from django.contrib.auth import get_user_model

class TripViewSet(viewsets.ModelViewSet):
    serializer_class = TripSerializer
    
    def get_queryset(self):
        # Eventually this will be filtered by request.user
        return Trip.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        # Temporarily assign the first user until auth is fully wired
        user = get_user_model().objects.first() 
        serializer.save(owner=user)

from rest_framework import generics
from .models import Activity
from .serializers import ActivitySerializer

# Handles GET /api/trips/<id>/activities/ and POST /api/trips/<id>/activities/
class TripActivityListCreateView(generics.ListCreateAPIView):
    serializer_class = ActivitySerializer

    def get_queryset(self):
        # Only return activities for the specific trip in the URL
        return Activity.objects.filter(trip_id=self.kwargs['trip_pk']).order_by('date', 'start_time')

# Handles PATCH /api/activities/<id>/ and DELETE /api/activities/<id>/
class ActivityRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer