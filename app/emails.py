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
    send_mail(subject, message, from_email, recipient_list, fail_silently=True)



def booking_cancellation_mail(booking):
    subject = "Booking Cancellation"
    message = f"Dear {booking.user.full_name()},\n\nYour Booking has been cancelled!\n\nBooking Details:\nDestination: {booking.tour.destination.name}\nJourney Date: {booking.tour.start_date}\nPickup Place: {booking.tour.start_place}\nPickup Time: {booking.tour.start_time}\n\nSorry for the inconveniences. We hope to see you again!\n\nBest regards,\nTravelBee Team"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [booking.user.user.email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=True)


def payment_confirmation_mail(payment):
    subject = "Payment Confirmation"
    message = f"Dear {payment.booking.user.full_name()},\n\nYour Payment for {payment.booking.tour.name} has been confirmed!\n\nPayment Details:\nPayment Method: {payment.payment_method}\nTransaction ID: {payment.transaction_id}\nPayment Number: 0{payment.payment_number}\nAmount: {payment.amount}\n\nWe look forward to seeing you!\n\nBest regards,\nTravelBee Team"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [payment.booking.user.user.email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=True)


def payment_failed_mail(payment):
    subject = "Payment Failed"
    message = f"Dear {payment.booking.user.full_name()},\n\nYour Payment for {payment.booking.tour.name} has failed!\n\nPayment Details:\nPayment Method: {payment.payment_method}\nTransaction ID: {payment.transaction_id}\nPayment Number: 0{payment.payment_number}\nAmount: {payment.amount}\n\nSorry for the inconveniences. We hope to see you again!\n\nBest regards,\nTravelBee Team"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [payment.booking.user.user.email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=True)