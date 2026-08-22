from rest_framework import viewsets
from django.db.models import Q
from .models import Destination
from .serializers import DestinationSerializer

class DestinationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DestinationSerializer

    def get_queryset(self):
        queryset = Destination.objects.all()
        
        # Handle React's search/filter query parameters
        search = self.request.query_params.get('search')
        category = self.request.query_params.get('category')
        min_rating = self.request.query_params.get('minRating')
        max_cost = self.request.query_params.get('maxCost')

        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(location__icontains=search))
        if category and category != 'all':
            queryset = queryset.filter(category=category)
        if min_rating:
            queryset = queryset.filter(rating__gte=float(min_rating))
        if max_cost:
            queryset = queryset.filter(estimated_cost__lte=float(max_cost))
            
        return queryset