import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date

# class RegistrationForm(forms.ModelForm):
#     confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput)
#
#     date_of_birth = forms.DateField(
#         label="Date of Birth",
#         widget=forms.SelectDateWidget(years=range(1950, 2010))
#     )
#
#     def clean_date_of_birth(self):
#         date_of_birth = self.cleaned_data.get('date_of_birth')
#         today = date.today()
#         age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
#
#         if age < 18:
#             raise ValidationError("You must be at least 18 years old to register.")
#
#         return date_of_birth
#
#     #
#     # phone_number = forms.CharField(
#     #     max_length=10,
#     #     label="Phone Number",
#     # )
#
#     # Add the "OTP" field
#     # otp = forms.CharField(
#     #     max_length=6,
#     #     label="OTP (One-Time Password)",
#     #     help_text="Enter the 6-digit OTP sent ."
#     # )
#
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email', 'password', 'date_of_birth']
#         widgets = {
#             'password': forms.PasswordInput,
#         }


# class ChangeForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email']
#
#
# # def clean_phone_number(self):
#     #     phone_number = self.cleaned_data.get('phone_number')
#     #
#     #     if not (6000000000 <= int(phone_number) <= 9999999999):
#     #         raise ValidationError("Phone number must be between 6,000,000,000 and 9,999,999,999")
#     #
#     #     return phone_number
#
#
# # class ChangeForm(forms.ModelForm):
# #     class Meta:
# #         model = User
# #         fields = ['username', 'first_name', 'last_name', 'email']







class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput)

    date_of_birth = forms.DateField(
        label="Date of Birth",
        widget=forms.SelectDateWidget(years=range(1950, 2010))
    )

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        today = date.today()
        age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))

        if age < 18:
            raise ValidationError("You must be at least 18 years old to register.")

        return date_of_birth

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if not re.match(r'^.*(?=.{8,})(?=.*\d)(?=.*[^\w\s]).*$', password):
            raise ValidationError("Password must be at least 8 characters with 1 special character.")

        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not re.match(r'^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$', email):
            raise ValidationError("Enter a valid email address (e.g., abc@gmail.com).")

        return email

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'date_of_birth']
        widgets = {
            'password': forms.PasswordInput,
        }

from django import forms
from django.contrib.auth.models import User

class PasswordResetForm(forms.Form):
    username_or_email = forms.CharField(label='Username or Email')

    def clean_username_or_email(self):
        username_or_email = self.cleaned_data['username_or_email']
        if '@' in username_or_email:
            user = User.objects.filter(email=username_or_email).first()
        else:
            user = User.objects.filter(username=username_or_email).first()
        if not user:
            raise forms.ValidationError('User does not exist')
        return user
class ChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']






