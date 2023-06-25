from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.utils.encoding import force_str
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,  DjangoUnicodeDecodeError
import django
if django.VERSION >= (3, 1):
    from django.utils.encoding import force_str
else:
    from django.utils.encoding import force_text
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import account_activation_token
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import threading
from django.contrib.auth import authenticate, login
from django.http import HttpResponse






class EmailThread(threading.Thread):


    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)


    def run(self):
        self.email.send(fail_silently=False)
      


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'sorry email in use,choose another one '}, status=409)
        return JsonResponse({'email_valid': True})


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric characters'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'sorry username in use,choose another one '}, status=409)
        return JsonResponse({'username_valid': True})


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        user, created = User.objects.get_or_create(username=username)

        if created:
            user.email = email
            user.set_password(password)
            user.save()

            current_site = get_current_site(request)
            email_body = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }

            link = reverse('activate', kwargs={
                           'uidb64': email_body['uid'], 'token': email_body['token']})

            email_subject = 'Activate your account'
            activate_url = 'http://'+current_site.domain+link

            email = EmailMessage(
                email_subject,
                'Hi '+user.username + ', Please click the link below to activate your account:\n'+activate_url,
                'shrestharajani155@gmail.com',
                [email],
            )

            EmailThread(email).start()
            messages.success(request, 'Account successfully created. Please check your email to activate your account.')
            return render(request, 'authentication/register.html')
        else:
            messages.error(request, 'Username is already taken')
            return render(request, 'authentication/register.html', context)
        
        # Add the following return statement
        return render(request, 'authentication/register.html', context)

            


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
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
                    messages.success(request, 'Welcome, ' +
                                     user.username+' you are now logged in')
                    return redirect('analysis')
                messages.error(
                    request, 'Account is not active,please check your email')
                return render(request, 'authentication/login.html')
            messages.error(
                request, 'Invalid credentials,try again')
            return render(request, 'authentication/login.html')

        messages.error(
            request, 'Please fill all fields')
        return render(request, 'authentication/login.html')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('login')


class RequestPasswordResetEmail(View):
    def get(self, request):
        
        return render(request,'authentication/reset-password.html')
    

    def post(self, request):

        #email = request.POST['email']
        email = request.POST.get('email')
        context = {
            'values': request.POST
        }
        

        if not validate_email(email):
            messages.error(request, 'Please supply a valid email')
            return render(request,'authentication/reset-password.html', context)


        current_site = get_current_site(request)
        user = User.objects.get(email=email)


       


        if user:
            email_contents = {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': PasswordResetTokenGenerator().make_token(user),
            }
            link = reverse('reset-user-password', kwargs={
                    'uidb64': email_contents['uid'], 'token': email_contents['token']})
            reset_url = 'http://{domain}{path}'.format(domain=current_site.domain, path=link)

            email = EmailMessage(
                    'Password Reset',
                    'Hi, Please click the link below to reset your password:\n{}'.format(reset_url),
                    'shrestharajani155@gmail.com',
                    [user.email],
            )
            EmailThread(email).start()

        messages.success(request, 'We have sent you an email to reset your password')
        return render(request,'authentication/reset-password.html')
        
        

class CompletePasswordReset(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(request, 'Password link is invalid, please request a new one')
                return render(request, 'authentication/reset-password.html')
         
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            messages.info(request, 'Password link is invalid, please request a new one')
            return render(request, 'authentication/reset-password.html')

        return render(request, 'authentication/set-new-password.html', context)
    
    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }

        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, 'Password do not match')
            return render(request, 'authentication/set-new-password.html', context)
        
        if len(password) < 6:
            messages.error(request, 'Password too short')
            return render(request, 'authentication/set-new-password.html', context)
        
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)

            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset success')
            return redirect('login')  
         
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            messages.info(request, 'Something went wrong, try again')
            return render(request, 'authentication/set-new-password.html', context)

        
            


def home(request):
    return render(request, 'authentication/home.html')

            
        
    


                    

           