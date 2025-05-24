from django.shortcuts import render, redirect
from django.utils.translation.trans_null import activate
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from gitdb.utils.encoding import force_text
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib import auth
from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_generator
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Sorry email in use, choose another one'}, status=409)
        return JsonResponse({'email_valid': True})

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should only contain alphanumeric characters'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Sorry username in use, choose another one'}, status=409)
        return JsonResponse({'username_valid': True})

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):

        # GET USER DATA
        # VALIDATE
        # CREATE A USER ACCOUNT

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():

                if len(password) < 8:
                    messages.error(request, 'Password must be at least 8 characters')
                    return render(request, 'authentication/register.html', context)

                user = User.objects.create_user(username=username, email=email, password=password)
                user.set_password(password)
                user.is_active = False
                user.save()

                # path to view
                # - getting domain we are on
                # - relative url to verification
                # - encode uid
                # - token
                # uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                # domain = get_current_site(request).domain
                # link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})
                # activate_url = 'http://' + domain + link
                # email_subject = 'Activate your account'
                # email_body = 'Hi' + user.username + 'Please use this link to verify your account\n' + activate_url
                # email = EmailMessage(
                #     email_subject,
                #     email_body,
                #     'noreply@example.com',
                #     [email],
                # )
                # email.send(fail_silently=False)
                messages.success(request, 'Your account has been created!')
                return render(request, 'authentication/register.html')



        return render(request, 'authentication/register.html')

class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                return redirect('login' + '?message' + 'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Your account has been activated successfully!')
            return redirect('login')

        except Exception as ex:
            pass
        return redirect('login')

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'You are now logged in! Welcome, ' + user.username)
                    return redirect('expenses')

                messages.error(request, 'Account is not active. Please check your email')
                return render(request, 'authentication/login.html')

            messages.error(request, 'Invalid Credentials. Try again')
            return render(request, 'authentication/login.html')

        messages.error(request, 'Please fill all fields')
        return render(request, 'authentication/login.html')

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out!')
        return redirect('login')

class RequestPasswordResetEmail(View):
    def get(self, request):
        return render(request, 'authentication/reset-password.html')
    def post(self, request):
        email = request.POST['email']

        context = {
            'values': request.POST
        }

        if not validate_email(email):
            messages.error(request, 'Email is invalid')
            return render(request, 'authentication/reset-password.html', context)

        current_site = get_current_site(request)
        user = request.objects.filter(email=email)

        if user.exists():
            email_contents = {
                'user': user[0],
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(user[0]),
            }

            link = reverse('reset-user-password', kwargs={
                'uidb64': email_contents['uid'], 'token': email_contents['token']
            })

            email_subject = 'Password reset instructions'

            reset_url = 'http://' + current_site.domain + link

            email = EmailMessage(
                email_subject,
                'Hi there, Please click the link below to reset your password \n' + reset_url,
                'noreply@semycolon.com',
                [email],
            )
            email.send(fail_silently=False)

        messages.success(request, 'We have sent you an email to reset your password')


        return render(request, 'authentication/reset-password.html')

class CompletePasswordReset(View):
    def get(self, request, uidb64, token):

        context = {
            'uidb64': uidb64,
            'token': token,
        }

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(request, 'Password link is invalid, please request a new one!')
                return render(request, 'authentication/reset-password.html')
        except Exception as ex:
            pass

        return render(request, 'authentication/set-new-password.html', context)
    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token,
        }
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'authentication/set-new-password.html', context)

        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters')
            return render(request, 'authentication/set-new-password.html', context)

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()

            messages.success(request, 'Your password has been updated!')
            return redirect('login')
        except Exception as identifier:
            messages.info(request, 'Something went wrong, try again!')
            return render(request, 'authentication/set-new-password.html', context)
        # return render(request, 'authentication/set-new-password.html', context)

