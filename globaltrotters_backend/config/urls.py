from django.contrib import admin
from django.urls import path, include
from trips.views import ActivityRetrieveUpdateDestroyView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/trips/", include("trips.urls")),
    path("api/destinations/", include("destinations.urls")),
    
    # Flat route for updating/deleting specific activities
    path("api/activities/<int:pk>/", ActivityRetrieveUpdateDestroyView.as_view(), name='activity-detail'),
]

from django.contrib import admin
from django.urls import path, include
from trips.views import ActivityRetrieveUpdateDestroyView, ExpenseRetrieveUpdateDestroyView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/trips/", include("trips.urls")),
    path("api/destinations/", include("destinations.urls")),
    
    path("api/activities/<int:pk>/", ActivityRetrieveUpdateDestroyView.as_view(), name='activity-detail'),
    # NEW: Flat route for updating/deleting specific expenses
    path("api/expenses/<int:pk>/", ExpenseRetrieveUpdateDestroyView.as_view(), name='expense-detail'),
]