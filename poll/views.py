from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .models import Candidate, ControlVote, Position
from .forms import ChangeForm

def homeView(request):
    return render(request, "poll/home.html")


from django.contrib.auth.models import User
from .forms import RegistrationForm

#
# from django.contrib.auth.models import User
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from .forms import RegistrationForm

from django.contrib import messages

from django.contrib import messages
import re


def registrationView(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']
            confirm_password = cd['confirm_password']

            # Check if user with the given username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken.')
                return render(request, "poll/registration.html", {'form': form})

            # Check if password matches confirm_password
            if password != confirm_password:
                messages.error(request, 'Password and confirmation password do not match.')
                form.add_error('confirm_password', 'Password and confirmation password do not match.')
                return render(request, "poll/registration.html", {'form': form})

            # Check if password length is at least 8 characters
            if len(password) < 8:
                messages.error(request, 'Password must be at least 8 characters long.')
                form.add_error('password', 'Password must be at least 8 characters long.')
                return render(request, "poll/registration.html", {'form': form,'password_match':True})

            # Check if password contains at least one special character
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                messages.error(request, 'Password must contain at least one special character.')
                form.add_error('password', 'Password must contain at least one special character.')
                return render(request, "poll/registration.html", {'form': form,'password_match':True})

            # If all validations pass, save the user
            user = form.save()
            user.set_password(password)
            user.save()

            return render(request, "poll/registration.html", {'form': form, 'registration_successful': True})

    else:
        form = RegistrationForm()

    # Modify email label to provide an example
    form.fields['email'].widget.attrs['placeholder'] = 'example@example.com'

    return render(request, "poll/registration.html", {'form': form})


def loginView(request):
    if request.method == "POST":
        user = request.POST.get('username')
        passw = request.POST.get('password')
        user = authenticate(request, username=user, password=passw)
        if user is not None:
            login(request,user)
            return redirect('dashboard')
        else:
            messages.success(request, 'Invalid username or password!')
            return render(request, "poll/login.html")
    else:
        return render(request, "poll/login.html")





# views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import PasswordResetForm

# def loginView(request):
#     if request.method == "POST":
#         usern = request.POST.get('username')
#         passw = request.POST.get('password')
#         user = authenticate(request, username=usern, password=passw)
#         if user is not None:
#             login(request, user)
#             return redirect('dashboard')
#         else:
#             messages.success(request, 'Invalid username or password!')
#             return render(request, "poll/login.html")
#     else:
#         # Include password reset form
#         password_reset_form = PasswordResetForm()
#         return render(request, "poll/login.html", {'password_reset_form': password_reset_form})

def changePassword(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            return redirect('dashboard')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, "poll/reset_password.html", {'form':form})

# views.py



#
# from django.contrib.auth.tokens import default_token_generator
# from django.utils.encoding import force_bytes
# from django.utils.http import urlsafe_base64_encode
# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.contrib.auth import update_session_auth_hash
# from django.contrib.auth.models import User
# from django.shortcuts import render, redirect
# from .forms import PasswordResetForm
#
# def password_reset(request):
#     if request.method == 'POST':
#         form = PasswordResetForm(request.POST)
#         if form.is_valid():
#             user = form.cleaned_data['username_or_email']
#             # Generate password reset token
#             token = default_token_generator.make_token(user)
#             uid = urlsafe_base64_encode(force_bytes(user.pk))
#             # Send password reset email
#             reset_link = request.build_absolute_uri(
#                 f'/password-reset-confirm/{uid}/{token}/'
#             )
#             send_mail(
#                 'Password Reset',
#                 render_to_string('email/password_reset_email.html', {'reset_link': reset_link}),
#                 'nimmagantiharika@gmail.com',
#                 [user.email],
#                 fail_silently=False,
#             )
#             return render(request, 'reset_password_sent.html')
#     else:
#         form = PasswordResetForm()
#     return render(request, 'reset_password.html', {'form': form})
#
# def password_reset_confirm(request, uidb64, token, user=None):
#     # Validate uidb64 and token, then render password reset form
#     # Verify token and uidb64 validity
#     ...
#     if request.method == 'POST':
#         # Handle password reset form submission
#         ...
#         # Update user's password
#         user.set_password(new_password)
#         user.save()
#         # Invalidate token
#         ...
#         # Redirect to login page or dashboard
#         return redirect('login')
#     return render(request, 'reset_password_confirm.html', {'uidb64': uidb64, 'token': token})
#

@login_required
def logoutView(request):
    logout(request)
    return redirect('home')
@login_required
def dashboardView(request):
    return render(request, "poll/dashboard.html")

@login_required
def positionView(request):

    obj = Position.objects.all()
    return render(request, "poll/position.html", {'obj':obj})
@login_required
def candidateView(request, pos):
    obj = get_object_or_404(Position, pk = pos)
    if request.method == "POST":
        temp = ControlVote.objects.get_or_create(user=request.user, position=obj)[0]
        if temp.status == False:
            temp2 = Candidate.objects.get(pk=request.POST.get(obj.title))
            temp2.total_vote += 1
            temp2.save()
            temp.status = True
            temp.save()
            return HttpResponseRedirect('/position/')
        else:
            messages.success(request, 'you have already been voted this position.')
            return render(request, 'poll/candidate.html', {'obj':obj})
    else:
        return render(request, 'poll/candidate.html', {'obj':obj})
@login_required
def resultView(request):
    obj = Candidate.objects.all().order_by('position','-total_vote')
    return render(request, "poll/result.html", {'obj':obj})

@login_required
def candidateDetailView(request, id):

    obj = get_object_or_404(Candidate, pk=id)
    return render(request, "poll/candidate_detail.html", {'obj':obj})
@login_required
def changePasswordView(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            return redirect('dashboard')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, "poll/password.html", {'form':form})
@login_required
def editProfileView(request):

    if request.method == "POST":
        form = ChangeForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ChangeForm(instance=request.user)
    return render(request, "poll/edit_profile.html", {'form':form})