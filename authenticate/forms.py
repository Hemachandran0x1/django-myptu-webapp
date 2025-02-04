from django import forms
from django.forms import ModelForm, Form
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from authenticate.models import Account

from django.conf import settings
import datetime


# Create the form class.

class UserRegisterForm(UserCreationForm):

    email = forms.EmailField(max_length=254, 
                             help_text='Required. Add a valid email address.')

    class Meta:
        model = Account
        fields = ('email', 
                  'username', 
                  'first_name', 
                  'last_name', 
                  'password1', 
                  'password2', )
        widgets = {
            'date_of_birth': forms.SelectDateWidget(years=range(2015, 1900, -1)),
            'create_password': forms.PasswordInput,
            'confirm_password': forms.PasswordInput
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        print(username, "validation username")
        if Account.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(f'Username {username} aldready exists')
        return username


    # def clean_date_of_birth(self):
    #     userAge = 13
    #     dob = self.cleaned_data.get('date_of_birth')
    #     today = datetime.date.today()
    #     if (dob.year + userAge, dob.month, dob.day) > (today.year, today.month, today.day):
    #         raise forms.ValidationError('user must be aged {} years and above.'. format(userAge))
    #     return dob

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Account.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(f'A email {email} has already registered.')
        return email

    def clean_password(self):
        '''
        we must ensure that both passwords are identical
        '''
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords must match')
        return password2

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        return first_name

    # def clean_contact(self):
    #     contact = self.cleaned_data.get('contact_number')
    #     if len(contact) < 10:
    #         raise forms.ValidationError('Enter a valid contact number')
    #     return contact
