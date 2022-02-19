from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse
import logging

# for login user
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# for email sending
from .models import User
from .utils import generate_token
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.conf import settings
import threading

# Create your views here.

logging.basicConfig(
    level=logging.ERROR,
    format="[%(asctime)s] Logging - %(message)s")

# Reducing Email Sending Time
class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

#activation email sending
def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('accounts/activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.EMAIL_FROM_USER,
                         to=[user.username]
                         )

    # if not settings.TESTING:
    EmailThread(email).start()


# Registration / Acccount creation
def register(request):
    # set the value of the username as the email input from the index.html for signup. If the value of your_email is empty, create the empty form without the pre-filled email value
    try:
        username = request.GET['your_email']
    except:
        username = ''

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        logging.debug(f':register:it is a post {form}')
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # Create user instance
            instance = form.save(commit=False)
            # instance.is_active = False
            logging.debug(
                f':register: account created with username as {username} and password is {password}')

            instance.save() #save user
            user = instance #initializing user
            send_activation_email(user, request) #sending email
            messages.success(request, f"Welcome {username}, your account has been created. \nWe've sent you an email to verify your account!")
            return redirect('accounts:login')
    else:
        if username == '':
            form = RegisterForm(request.POST)
        else:
            form = RegisterForm(
                initial={'username': request.GET['your_email']})

        logging.debug('register: it is a get')

    return render(request, 'accounts/register.html', {'form': form})

# Activating user
def activate_user(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.is_active = True
        user.save()
        messages.success(request, 'Email verified, you can now login')
        return redirect('accounts:login')

    return render(request, 'accounts/activate_failed.html', {"user": user})


# Login/authentication View
def login_user(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        # context = {'data': request.POST}
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user and not user.is_email_verified:
                form = AuthenticationForm()
                messages.warning(request,'Email is not verified, please check your email inbox')
                return render(request, 'accounts/login.html',{"form":form})

            if not user:
                form = AuthenticationForm()
                messages.error(request, 'Invalid credentials, try again')
                return render(request, 'accounts/login.html', {"form":form})

            login(request, user)
            messages.success(request, f"Welcome {user.username}" )

            return redirect('index')

    return render(request, 'accounts/login.html', {"form":form})

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect('index')