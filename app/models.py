from collections.abc import Iterable
from datetime import date
from django.forms import ValidationError
from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import User
from .emails import *


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=200)
    nid = models.CharField(max_length=10, blank=True, null=True)
    image = models.ImageField(upload_to='images/user/', blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    def full_name(self):
        return self.user.first_name + ' ' + self.user.last_name
    

class Guide(models.Model):
    user = models.OneToOneField(User, related_name='guide', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/guides/', blank=True, null=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=11)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=200)
    nid = models.CharField(max_length=17, blank=True, null=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    def updateRating(self, rating):
        self.rating = rating
        self.save()

    def save(self, *args, **kwargs):
        first_name, last_name = self.name.split(' ', 1)
        self.user.first_name = first_name
        self.user.last_name = last_name
        email = self.email
        self.user.email = email
        self.email = email
        self.user.save()
        super(Guide, self).save(*args, **kwargs)

    def total_reviews(self):
        return self.reviews.count()


class Place(models.Model):
    name = models.CharField(max_length=200)
    description = RichTextField()
    map_link = models.URLField(max_length=500, blank=True, null=True)
    def __str__(self):
        return self.name
    
    def total_images(self):
        return self.images.count()
    
    def featured_image(self):
        return self.images.first().image
    
    def upcoming_tours(self):
        return self.tours.filter(status='announced' or 'booking')
    
    def upcoming_tours_count(self):
        return self.upcoming_tours().count()
    
    def has_map(self):
        return True if self.map_link else False
    
    def calculate_rating(self):
        total = 0
        for tour in self.tours.all():
            total += tour.rating()
        return 0 if self.tours.count()==0 else total / self.tours.count()
    
    def rounded_rating(self):
        return int(round(self.calculate_rating(), 0))


class PlaceImage(models.Model):
    image = models.ImageField(upload_to='images/places/')
    place = models.ForeignKey('Place', related_name='images', on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.place.name


class TourType(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    

class Tour(models.Model):
    STATUS_CHOICES = (
        ('announced', 'Announced'),
        ('booking', 'Booking'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    name = models.CharField(max_length=200)
    tour_type = models.ForeignKey('TourType', on_delete=models.CASCADE, blank=True, null=True)
    destination = models.ForeignKey('Place', related_name='tours', on_delete=models.CASCADE, blank=True, null=True)
    guide = models.ForeignKey('Guide', related_name='tours', on_delete=models.CASCADE, blank=True, null=True)
    total_seats = models.IntegerField()
    days = models.IntegerField()
    price = models.IntegerField()
    min_age = models.IntegerField()
    max_age = models.IntegerField(null=True, blank=True)
    start_date = models.DateField()
    start_time = models.TimeField()
    start_place = models.CharField(max_length=200)
    end_date = models.DateField()
    end_time = models.TimeField()
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='announced')
    featured_image = models.ImageField(upload_to='images/tours/', blank=True, null=True)

    def __str__(self):
        return self.name
    
    def total_bookings(self):
        bookings = 0
        for booking in self.bookings.all().exclude(status='cancelled'):
            bookings += booking.total_person
        return bookings
    
    def is_expired(self):
        return True if self.start_date < date.today() else False
        
    
    def available_seats(self):
        return self.total_seats - self.total_bookings()
    
    def minimum_advance(self):
        return self.price * 0.2
    
    def rating(self):
        total = 0
        for review in self.reviews.all():
            total += review.rating
        return 0 if self.reviews.count()==0 else total / self.reviews.count()
    

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey('Profile', related_name='bookings', on_delete=models.CASCADE, blank=True, null=True)
    tour = models.ForeignKey('Tour', related_name="bookings", on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_person = models.IntegerField(default=1)
    total_price = models.IntegerField(default=0, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    phone1 = models.CharField(max_length=11, blank=True, null=True)
    phone2 = models.CharField(max_length=11)

    def __str__(self):
        return f'{self.user.user.username}: {self.tour.name}'
    
    def updateStatus(self, status):
        self.status = status
        self.save()

    def save(self, *args, **kwargs):
        self.total_price = self.tour.price * self.total_person
        print(self.rents.count())
        if self.id:
            if self.rents.count()>0:
                self.total_price+=sum([rent.amount for rent in self.rents.all()])
        if self.phone1 is None:
            self.phone1 = self.user.phone
        if self.status=='confirmed':
            booking_confirmation_mail(self)
        elif self.status=='cancelled':
            booking_cancellation_mail(self)
        super(Booking, self).save(*args, **kwargs)

    def paid_amount(self):
        total = 0
        for payment in self.payments.filter(status='confirmed'):
            total += payment.amount
        return total
    
    def due_amount(self):
        return self.total_price - self.paid_amount()

    def calculate_due(self):
        return self.total_price - self.paid_amount()
    

class BookingPayment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('bkash', 'Bkash'),
        ('rocket', 'Rocket'),
        ('nagad', 'Nagad'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('failed', 'Failed'),
    ]
    booking = models.ForeignKey('Booking', related_name='payments', on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=200)
    payment_number = models.IntegerField()
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.booking.user.user.username
    
    def save(self, *args, **kwargs):
        if self.status=='confirmed':
            payment_confirmation_mail(self)
        elif self.status=='failed':
            payment_failed_mail(self)
        super(BookingPayment, self).save(*args, **kwargs)



class Review(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE, blank=True, null=True)
    tour = models.ForeignKey('Tour',related_name='reviews', on_delete=models.CASCADE, blank=True, null=True)
    rating = models.IntegerField(default=0)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.user.username
    
    def save(self, *args, **kwargs):
        super(Review, self).save(*args, **kwargs)
        self.tour.guide.updateRating(self.rating)
    
    def updateRating(self, rating):
        self.rating = rating
        self.save()
        self.tour.guide.updateRating(self.rating)



class ReviewImage(models.Model):
    image = models.ImageField(upload_to='images/reviews/')
    review = models.ForeignKey('Review', related_name='images', on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.review.user.user.username
    

class GuideReview(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE, blank=True, null=True)
    guide = models.ForeignKey('Guide',related_name='reviews', on_delete=models.CASCADE, blank=True, null=True)
    rating = models.IntegerField(default=0)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.user.username
    
    def save(self, *args, **kwargs):
        super(GuideReview, self).save(*args, **kwargs)

    

def user_type(user):
    if hasattr(user, 'profile'):
        return 'User'
    elif hasattr(user, 'guide'):
        return 'Guide'
    else:
        return 'Staff'
    

User.add_to_class('user_type', user_type)


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    image = models.ImageField(upload_to='images/products/')
    stock = models.IntegerField(default=1)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    def available_stock(self):
        return self.stock - sum([rent.quantity for rent in self.rents.all()])
    

class Rent(models.Model):
    booking = models.ForeignKey('Booking', related_name='rents', on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey('Product', related_name='rents', on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    days = models.IntegerField(default=1)
    amount = models.IntegerField(default=0, null=True, blank=True)
    def __str__(self):
        return f'{self.product.name} For {self.booking.tour.name}'
    
    def save(self, *args, **kwargs):
        self.amount = self.product.price * self.quantity * self.days
        super(Rent, self).save(*args, **kwargs)
        self.booking.save()