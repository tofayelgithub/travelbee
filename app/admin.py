from django.contrib import admin
from .models import *
from django.urls import reverse
from django.utils.safestring import mark_safe

#custom user admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


admin.site.site_header = 'TravelBee Administration'
admin.site.site_title = 'TravelBee Admin'
admin.site.index_title = 'Admin Panel'

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

class GuideInline(admin.StackedInline):
    model = Guide
    can_delete = False
    verbose_name_plural = 'guide'

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'user_type')
    inlines = (ProfileInline, GuideInline, )

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


admin.site.register(Profile)





class GuideAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'address', 'nid', 'rating')
    search_fields = ['name', 'phone', 'address', 'nid']
    list_filter = ['rating']
    ordering = ['name']
    list_per_page = 10

admin.site.register(Guide, GuideAdmin)


class PlaceImageInline(admin.TabularInline):
    model = PlaceImage

class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_images')
    search_fields = ['name']
    list_filter = ['name']
    ordering = ['name']
    list_per_page = 10
    inlines = [PlaceImageInline]


admin.site.register(Place, PlaceAdmin)

admin.site.register(TourType)


class BookingInline(admin.TabularInline):
    model = Booking
    readonly_fields = ('paid_amount', 'due_amount','view_details')
    can_delete = False
    verbose_name_plural = 'bookings'

    def view_details(self, obj):
        view_url = reverse("admin:app_booking_change", args=[obj.id])
        return mark_safe("<a href='{}'>View Details</a>".format(view_url))




class TourAdmin(admin.ModelAdmin):
    list_display = ('name', 'tour_type', 'total_bookings', 'available_seats')
    readonly_fields = ('total_bookings', 'available_seats')
    search_fields = ['name', 'tour_type__name']
    list_filter = ['tour_type__name']
    ordering = ['name']
    list_per_page = 10
    inlines = [BookingInline]

admin.site.register(Tour, TourAdmin)




admin.site.register(BookingPayment)
class PaymentInline(admin.TabularInline):
    model = BookingPayment
    readonly_fields = ('view_details',)
    can_delete = False
    verbose_name_plural = 'payments'

    def view_details(self, obj):
        view_url = reverse("admin:app_bookingpayment_change", args=[obj.id])
        return mark_safe("<a href='{}'>View Details</a>".format(view_url))
    

class RentInline(admin.TabularInline):
    model = Rent
    readonly_fields = ('view_details',)
    can_delete = False
    verbose_name_plural = 'rents'

    def view_details(self, obj):
        view_url = reverse("admin:app_rent_change", args=[obj.id])
        return mark_safe("<a href='{}'>View Details</a>".format(view_url))

class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour', 'status', 'created_at', 'paid_amount')
    readonly_fields = ('paid_amount', 'due_amount', 'created_at')
    search_fields = ['user__username', 'tour__name']
    list_filter = ['status', 'created_at']
    ordering = ['created_at']
    list_per_page = 10
    inlines = [PaymentInline, RentInline]

admin.site.register(Booking, BookingAdmin)



class ReviewImageInline(admin.TabularInline):
    model = ReviewImage

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'created_at')
    search_fields = ['user__username']
    list_filter = ['created_at']
    ordering = ['created_at']
    list_per_page = 10
    inlines = [ReviewImageInline]

admin.site.register(Review, ReviewAdmin)

class GuideReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'guide', 'rating', 'created_at')
    search_fields = ['user__username', 'guide__name']
    list_filter = ['created_at']
    ordering = ['created_at']
    list_per_page = 10

admin.site.register(GuideReview, GuideReviewAdmin)


class ProductRentInline(admin.TabularInline):
    model = Rent
    readonly_fields = ('view_details',)
    can_delete = False
    verbose_name_plural = 'rents'

    def view_details(self, obj):
        view_url = reverse("admin:app_rent_change", args=[obj.id])
        return mark_safe("<a href='{}'>View Details</a>".format(view_url))
    

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']
    list_filter = ['name']
    ordering = ['name']
    list_per_page = 10
    inlines = [ProductRentInline]

admin.site.register(Product, ProductAdmin)



class RentAdmin(admin.ModelAdmin):
    list_display = ('product', 'booking', 'quantity')
    search_fields = ['booking__user', 'product__name']
    list_filter = ['product__name', 'booking__user', 'booking__tour']
    list_per_page = 10

admin.site.register(Rent, RentAdmin)