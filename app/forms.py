from django import forms
from django.contrib.auth.models import User
from .models import Profile, Booking, BookingPayment

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5',
                                               'placeholder': 'username',
                                               'required':'true',
                                               }),
            'email': forms.EmailInput(attrs={'class': 'form-input bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5',
                                             'placeholder': 'name@gmail.com',
                                               'required':'true',}),
            'password': forms.PasswordInput(attrs={'class': 'form-input bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5',
                                                   'placeholder': '••••••••',
                                                    'required':'true',
                                                    'pattern':'(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}',
                                                    'title':'Must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters',
                                                   }),
            'first_name': forms.TextInput(attrs={'class': 'form-input bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5',
                                                    'placeholder': 'First Name',
                                                    'required':'true',
                                                    }),
            'last_name': forms.TextInput(attrs={'class': 'form-input bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5',
                                                    'placeholder': 'Last Name',
                                                    }),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'nid', 'image']

        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-input bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5',
                                            'placeholder': '01700000000',
                                            'title':'Phone number must be 11 digits',
                                            'pattern':'[0-9]{11}',

                                            }),
            'address': forms.TextInput(attrs={'class': 'form-input bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5', 'placeholder': 'Your Address'}),
            'nid': forms.TextInput(attrs={'class': 'form-input bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5',
                                          'placeholder': '0123456789',
                                            'title':'NID number must be 10 digits',
                                            'pattern':'[0-9]{10}',
                                          }),
            'image': forms.ClearableFileInput(attrs={'class': 'form-input bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full'}),
        }
        

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'nid', 'image']






class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['total_person', 'phone1', 'phone2']


class PaymentForm(forms.ModelForm):
    class Meta:
        model = BookingPayment
        fields = ['payment_method', 'transaction_id', 'payment_number', 'amount']