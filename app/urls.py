from django.urls import path
from .views import *

urlpatterns = [
    path('', indexView, name='index'),
    path('search/', searchView, name='search'),
    
    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),
    path('register/', registerView, name='register'),

    path('destinations/', destinationsListView, name='destination'),
    path('destinations/<int:pk>/', destinationDetailView, name='destination_detail'),

    path('guides/', guidesListView, name='guide'),
    path('guides/<int:pk>/', guideDetailView, name='guide_detail'),

    path('tours/', toursListView, name='tour'),
    path('tours/<int:pk>/', tourDetailView, name='tour_detail'),
    path('tours/<int:pk>/booking/', bookATourView, name='tour_book'),

    path('profile/', profileView, name='profile'),
    path('profile/settings/', profileSettingsView, name='profile_settings'),
    path('profile/bookings/', bookingListView, name='bookings'),
    path('profile/bookings/<int:pk>/', bookingDetailView, name='booking_detail'),
]
