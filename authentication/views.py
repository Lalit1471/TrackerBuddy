from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import auth, messages
from validate_email import validate_email
from django.core.mail import EmailMessage


# Create your views here.
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
            return JsonResponse({'username_error': 'sorry username in use,choose another one!'}, status=409)
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

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/register.html', context)
                elif len(username) == 0:
                    messages.error(request, 'Enter a valid username')
                    return render(request, 'authentication/register.html', context)
                elif len(email) == 0:
                    messages.error(request, 'Enter a valid email')
                    return render(request, 'authentication/register.html', context)
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    messages.success(request, 'Registered Successfully', context)
                    return render(request, 'authentication/register.html')
        else:
            messages.error(request, 'Username not available')
            return render(request, 'authentication/register.html', context)
        return render(request, 'authentication/register.html')
