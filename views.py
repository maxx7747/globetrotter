

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

from .models import Expense
from .serializers import ExpenseSerializer

# Handles GET /api/trips/<id>/expenses/ and POST /api/trips/<id>/expenses/
class TripExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        # Return expenses only for the trip specified in the URL
        return Expense.objects.filter(trip_id=self.kwargs['trip_pk']).order_by('-date', '-created_at')

# Handles PATCH /api/expenses/<id>/ and DELETE /api/expenses/<id>/
class ExpenseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import TripCollaborator
from .serializers import TripSerializer, ActivitySerializer, ExpenseSerializer, TripCollaboratorSerializer

# --- COMMUNITY VIEWS ---
class CommunityTripListView(generics.ListAPIView):
    serializer_class = TripSerializer

    def get_queryset(self):
        queryset = Trip.objects.filter(is_public=True)
        
        search = self.request.query_params.get('search')
        sort_by = self.request.query_params.get('sortBy', 'popular')

        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(stops__destination_name__icontains=search)).distinct()

        if sort_by == 'recent':
            queryset = queryset.order_by('-created_at')
        elif sort_by == 'budget-low':
            queryset = queryset.order_by('budget')
        elif sort_by == 'budget-high':
            queryset = queryset.order_by('-budget')
        else: # popular
            queryset = queryset.order_by('-likes', '-views')
            
        return queryset

class TripCloneView(APIView):
    def post(self, request, trip_pk):
        try:
            original_trip = Trip.objects.get(pk=trip_pk, is_public=True)
        except Trip.DoesNotExist:
            return Response({"detail": "Trip not found or not public."}, status=status.HTTP_404_NOT_FOUND)
        
        # Clone the trip
        cloned_trip = Trip.objects.create(
            owner=request.user if request.user.is_authenticated else get_user_model().objects.first(),
            name=f"Copy of {original_trip.name}",
            start_date=original_trip.start_date,
            end_date=original_trip.end_date,
            budget=original_trip.budget,
            currency=original_trip.currency,
            status='draft',
            is_public=False,
            travelers=original_trip.travelers,
            notes=original_trip.notes
        )

        # Clone the stops
        for stop in original_trip.stops.all():
            stop.pk = None
            stop.trip = cloned_trip
            stop.save()

        return Response(TripSerializer(cloned_trip).data, status=status.HTTP_201_CREATED)

# --- COLLABORATOR VIEWS ---
class CollaboratorListCreateView(APIView):
    def post(self, request, trip_pk):
        email = request.data.get('email')
        User = get_user_model()
        user = User.objects.filter(email=email).first()
        
        if not user:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            
        trip = Trip.objects.get(pk=trip_pk)
        collaborator, created = TripCollaborator.objects.get_or_create(
            trip=trip, user=user, defaults={'role': 'editor'}
        )
        return Response(TripCollaboratorSerializer(collaborator).data, status=status.HTTP_201_CREATED)

class CollaboratorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TripCollaborator.objects.all()
    serializer_class = TripCollaboratorSerializer