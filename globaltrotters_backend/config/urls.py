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

from trips.views import ActivityRetrieveUpdateDestroyView, ExpenseRetrieveUpdateDestroyView, CollaboratorRetrieveUpdateDestroyView, CommunityTripListView, TripCloneView
from accounts.views import UserProfileView, UserSearchView

urlpatterns = [
    # ... existing routes ...
    path("api/activities/<int:pk>/", ActivityRetrieveUpdateDestroyView.as_view(), name='activity-detail'),
    path("api/expenses/<int:pk>/", ExpenseRetrieveUpdateDestroyView.as_view(), name='expense-detail'),
    path("api/collaborators/<int:pk>/", CollaboratorRetrieveUpdateDestroyView.as_view(), name='collaborator-detail'),
    
    # Community
    path("api/community/trips/", CommunityTripListView.as_view(), name='community-trips'),
    path("api/community/trips/<int:trip_pk>/clone/", TripCloneView.as_view(), name='trip-clone'),

    # Users
    path("api/users/me/", UserProfileView.as_view(), name='user-profile'),
    path("api/users/search/", UserSearchView.as_view(), name='user-search'),
]