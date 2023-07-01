from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import *
from .models import *
from django.db.models import Q


# Create your views here.

def indexView(request):
    data = {}
    data['upcoming_tours'] = Tour.objects.filter(Q(status='announced') | Q(status='booking')).order_by('-id')
    data['popular_destinations'] = Place.objects.all().order_by('-id')[:5]
    return render(request, 'landing/index.html', data)


"""
Authentication
"""

def loginView(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin:index')
        else:
            return redirect('index')
        
    data = {}
    if request.method == 'POST':
        print(request.POST)
        data['password'] = request.POST.get('password')
        data['username'] = User.objects.get(email=request.POST.get('email')).username
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'auth/login.html', {'error': 'Invalid username or password'})

    return render(request, 'auth/login.html')


def logoutView(request):
    logout(request)
    return redirect('index')


def registerView(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            user = authenticate(username=user_form.cleaned_data['username'], password=user_form.cleaned_data['password'])
            login(request, user)
            return redirect('index')
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileForm()
    return render(request, 'auth/register.html', {'user_form': user_form, 'profile_form': profile_form})


def searchView(request):
    tours = Tour.objects.all().order_by('-id')
    try:
        destination = Place.objects.get(pk=int(request.GET.get('destination')))
        tours = tours.filter(place=destination)
    except:
        pass
    try:
        tourtype = TourType.objects.get(pk=int(request.GET.get('tourtype')))
        tours = tours.filter(tour_type=tourtype)
    except:
        pass
    return render(request, 'landing/index.html', {'tours': tours})




"""
Destinations
"""

def destinationsListView(request):
    destinations = Place.objects.all()
    return render(request, 'landing/destinations/list.html', {'destinations': destinations})


def destinationDetailView(request, pk):
    destination = Place.objects.get(pk=pk)
    return render(request, 'landing/destinations/detail.html', {'destination': destination})



"""
Tour Guides
"""

def guidesListView(request):
    guides = Guide.objects.all()
    return render(request, 'landing/guides/list.html', {'guides': guides})


def guideDetailView(request, pk):
    guide = Guide.objects.get(pk=pk)
    tour = guide.tours.first()
    print(tour.destination.featured_image())
    return render(request, 'landing/guides/detail.html', {'guide': guide})


"""
Tours
"""


def toursListView(request):
    tours = Tour.objects.all().order_by('-id')
    if request.GET.get('destination') and request.GET.get('destination') !="0":
        destination = Place.objects.get(pk=int(request.GET.get('destination')))
        tours = tours.filter(destination=destination)
    if request.GET.get('tourtype') and request.GET.get('tourtype') !="0":
        tourtype = TourType.objects.get(pk=int(request.GET.get('tourtype')))
        tours = tours.filter(tour_type=tourtype)
    return render(request, 'landing/tours/list.html', {'tours': tours})


def tourDetailView(request, pk):
    tour = Tour.objects.get(pk=pk)
    return render(request, 'landing/tours/detail.html', {'tour': tour})






def bookATourView(request, pk):
    data = {}
    tour = Tour.objects.get(pk=pk)
    user = request.user.profile
    data['tour'] = tour
    if request.method == 'POST':
        print(request.POST)
        booking_form = BookingForm(request.POST)
        print(booking_form)
        payment_form = PaymentForm(request.POST)
        if booking_form.is_valid():
            booking = booking_form.save(commit=False)
            booking.tour = tour
            booking.user = user
            booking.save()
            payment = payment_form.save(commit=False)
            payment.booking = booking
            payment.save()
            return redirect('index')
        else:
            data['errors'] = True
            data['booking_form_errors'] = booking_form.errors
            data['payment_form_errors'] = payment_form.errors


        
    return render(request, 'landing/tours/book.html', data)


"""
User Profile
"""

def profileView(request):
    data = {'title': "Your Profile"}
    if request.method == 'POST':
        action = request.POST.get('action') 
        if action == 'updateUser':
            user_form = UserUpdateForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                return redirect('profile')
            else:
                data['user_errors'] = user_form.errors
        elif action == 'updateProfile':
            print(request.FILES)
            profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            if profile_form.is_valid():
                profile_form.save()
                return redirect('profile')
            else:
                data['profile_errors'] = profile_form.errors
    return render(request, 'profile/index.html',data)

def profileSettingsView(request):
    data = {'title': "Settings"}
    if request.method == 'POST':
        user = request.user
        if user.check_password(request.POST.get('old_password')):
            if request.POST.get('new_password') == request.POST.get('confirm_password'):
                user.set_password(request.POST.get('new_password'))
                user.save()
                return redirect('index')
            else:
                data['error'] = 'New password and confirm password does not match'
                return render(request, 'profile/settings.html', data)
        else:
            data['error'] = 'Old password is incorrect'
            return render(request, 'profile/settings.html',data)
    return render(request, 'profile/settings.html', data)


def bookingListView(request):
    data = {'title': "Your Bookings"}
    data['bookings'] = Booking.objects.filter(user=request.user.profile).exclude(Q(tour__status='completed') | Q(tour__status='cancelled')).exclude(status='cancelled')
    data['old_bookings'] = Booking.objects.filter(user=request.user.profile, tour__status='completed')
    data['cancelled_bookings'] = Booking.objects.filter(user=request.user.profile, status='cancelled')
    return render(request, 'profile/booking.html', data)


def bookingDetailView(request, pk):
    data = {}
    data['booking'] = Booking.objects.get(pk=pk)
    data['title']= f"Booking: {data['booking'].tour.name}"
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.booking = data['booking']
            payment.save()
            return redirect('booking_detail')
        else:
            data['errors'] = form.errors
    return render(request, 'profile/booking_detail.html', data)
