from django.core.mail import send_mail
from django.conf import settings

def booking_confirmation_mail(booking):
    booking_details = {
        'name': booking.user.full_name(),
        'destination': booking.tour.destination.name,
        'journey_date': booking.tour.start_date,
        'pickup_place': booking.tour.start_place,
        'pickup_time': booking.tour.start_time,
    }
    subject = 'Booking Confirmation'
    message = f"Dear {booking_details['name']},\n\nYour Booking has been confirmed!\n\nBooking Details:\nDestination: {booking_details['destination']}\nJourney Date: {booking_details['journey_date']}\nPickup Place: {booking_details['pickup_place']}\nPickup Time: {booking_details['pickup_time']}\n\nWe look forward to seeing you!\n\nBest regards,\nTravelBee Team"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [booking.user.user.email]
    send_mail(subject, message, from_email, recipient_list)