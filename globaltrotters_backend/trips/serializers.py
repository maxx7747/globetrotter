from rest_framework import serializers
from .models import Trip, TripStop

class TripStopSerializer(serializers.ModelSerializer):
    # Mapping camelCase from React to snake_case in Django
    destinationName = serializers.CharField(source='destination_name')
    startDate = serializers.DateField(source='start_date', required=False, allow_null=True)
    endDate = serializers.DateField(source='end_date', required=False, allow_null=True)

    class Meta:
        model = TripStop
        fields = ['id', 'destinationName', 'country', 'order', 'startDate', 'endDate', 'lat', 'lng', 'notes']

class TripSerializer(serializers.ModelSerializer):
    stops = TripStopSerializer(many=True)
    ownerId = serializers.IntegerField(source='owner.id', read_only=True)
    startDate = serializers.DateField(source='start_date', required=False, allow_null=True)
    endDate = serializers.DateField(source='end_date', required=False, allow_null=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Trip
        fields = ['id', 'ownerId', 'name', 'startDate', 'endDate', 'budget', 'currency', 'status', 'is_public', 'travelers', 'notes', 'stops', 'createdAt']
        read_only_fields = ['id', 'createdAt']

    def create(self, validated_data):
        stops_data = validated_data.pop('stops', [])
        
        if validated_data.get('start_date'):
            validated_data['status'] = 'upcoming'

        trip = Trip.objects.create(**validated_data)
        
        for stop_data in stops_data:
            TripStop.objects.create(trip=trip, **stop_data)
            
        return trip

from .models import Activity

class ActivitySerializer(serializers.ModelSerializer):
    tripId = serializers.PrimaryKeyRelatedField(source='trip', queryset=Trip.objects.all())
    stopId = serializers.PrimaryKeyRelatedField(source='stop', queryset=TripStop.objects.all())
    startTime = serializers.TimeField(source='start_time', format='%H:%M', input_formats=['%H:%M'])
    endTime = serializers.TimeField(source='end_time', format='%H:%M', input_formats=['%H:%M'], required=False, allow_null=True)
    estimatedCost = serializers.DecimalField(source='estimated_cost', max_digits=10, decimal_places=2, required=False)

    class Meta:
        model = Activity
        fields = ['id', 'tripId', 'stopId', 'name', 'category', 'date', 'startTime', 'endTime', 'estimatedCost', 'notes', 'location']