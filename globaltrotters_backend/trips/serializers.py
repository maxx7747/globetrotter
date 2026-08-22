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

from .models import Expense

class ExpenseSerializer(serializers.ModelSerializer):
    tripId = serializers.PrimaryKeyRelatedField(source='trip', queryset=Trip.objects.all())
    stopId = serializers.PrimaryKeyRelatedField(source='stop', queryset=TripStop.objects.all(), required=False, allow_null=True)
    isEstimate = serializers.BooleanField(source='is_estimate')

    class Meta:
        model = Expense
        fields = ['id', 'tripId', 'stopId', 'category', 'amount', 'date', 'description', 'isEstimate']

from .models import TripCollaborator # Add this import at the top

# Add this new serializer before TripSerializer
class TripCollaboratorSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(source='user.id', read_only=True)
    # Adjust 'first_name' to match your Custom User model's name field if necessary
    fullName = serializers.CharField(source='user.first_name', read_only=True) 
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = TripCollaborator
        fields = ['id', 'userId', 'fullName', 'email', 'role']

# Update your existing TripSerializer to include the new fields
class TripSerializer(serializers.ModelSerializer):
    stops = TripStopSerializer(many=True, required=False)
    collaborators = TripCollaboratorSerializer(many=True, read_only=True)
    ownerId = serializers.IntegerField(source='owner.id', read_only=True)
    ownerName = serializers.CharField(source='owner.first_name', read_only=True)
    startDate = serializers.DateField(source='start_date', required=False, allow_null=True)
    endDate = serializers.DateField(source='end_date', required=False, allow_null=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Trip
        fields = ['id', 'ownerId', 'ownerName', 'name', 'startDate', 'endDate', 'budget', 'currency', 'status', 'is_public', 'travelers', 'notes', 'stops', 'collaborators', 'createdAt', 'likes', 'views']
        read_only_fields = ['id', 'createdAt', 'likes', 'views']

    # ... keep your existing create() method exactly as it is ...