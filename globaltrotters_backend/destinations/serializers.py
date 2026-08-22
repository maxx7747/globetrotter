from rest_framework import serializers
from .models import Destination

class DestinationSerializer(serializers.ModelSerializer):
    estimatedCost = serializers.DecimalField(source='estimated_cost', max_digits=10, decimal_places=2)

    class Meta:
        model = Destination
        fields = ['id', 'name', 'location', 'category', 'rating', 'estimatedCost', 'currency', 'description', 'image', 'lat', 'lng']