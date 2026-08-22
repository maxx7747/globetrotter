from django.db import models

class Destination(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    category = models.CharField(max_length=50)
    rating = models.FloatField(default=0.0)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default="INR")
    description = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.location}"