from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Trip(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trips")
    name = models.CharField(max_length=255)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default="INR")
    status = models.CharField(max_length=20, default="draft")
    is_public = models.BooleanField(default=False)
    travelers = models.IntegerField(default=1)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class TripStop(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="stops")
    destination_name = models.CharField(max_length=255)
    country = models.CharField(max_length=255, blank=True, null=True)
    order = models.IntegerField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)


class Activity(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="activities")
    stop = models.ForeignKey(TripStop, on_delete=models.CASCADE, related_name="activities")
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name} on {self.date}"