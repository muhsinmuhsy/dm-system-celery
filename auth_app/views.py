from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError

def customer_signup(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')

            if password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return redirect('customer_signup')

            # Check if the email is already taken
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists.')
                return redirect('customer_signup')

            # Create the user
            user = User.objects.create_user(
                email=email, 
                password=password,
                first_name=first_name, 
                last_name=last_name,
                is_customer=True
            )
            user.save()
            
            # Log the user in after registration
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'signuped Successfully and logged in.')
                return redirect('home')
            else:
                messages.error(request, 'Authentication failed.')
                return redirect('customer_signup')

        except ValidationError as e:
            messages.error(request, f'Validation error: {e}')
            return redirect('customer_signup')
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')
            return redirect('customer_signup')

    return render(request, 'auth_app/customer_signup.html')


def customer_signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, 'Email and password are required.')
            return redirect('customer_signin')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Email does not exist.')
            return redirect('customer_signin')

        if user.check_password(password):
            authenticated_user = authenticate(request, email=email, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                messages.success(request, 'signin successful.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid signin credentials.')
        else:
            messages.error(request, 'Incorrect password.')

    return render(request, 'auth_app/customer_signin.html')

def logout_view(request):
    try:
        logout(request)
        messages.success(request, 'Logged out successfully.')
    except Exception as e:
        messages.error(request, 'Logout failed. Please try again.')
    return redirect('home')



    