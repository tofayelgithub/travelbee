from .models import Tour, Place, TourType
from django.db.models import Q

# def tourtypes(request):
#     return {'tourtypes': TourType.objects.all()}

def context(request):
    data = {
        'destinations': Place.objects.all(),
        'upcoming_tours': Tour.objects.filter(Q(status='announced') | Q(status='booking')).order_by('-id'),
        'tourtypes': TourType.objects.all()
    }
    return data