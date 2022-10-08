from django.shortcuts import redirect, render
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout

from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user

User = get_user_model()

def home(request):
    return render(request, 'index.html')

@unauthenticated_user
def sign_up(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        user = User(username = username, email = email)
        if user_type == "student":
            user.is_student = True
        user.set_password(password)
        user.save()
        if user := authenticate(username=user.username, password=password):
            login(request, user)
            messages.success(request, "Account created successfully")
            return redirect('home')

    return render(request, 'sign_up.html')

@unauthenticated_user
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            if user := authenticate(username=username, password=password):
                login(request, user)
                messages.success(request, "Login successful")
                return redirect('home')
            else:
                messages.error(request, 'Inavlid username or password. Try again!')
    else:
        form  = AuthenticationForm()
    return render(request,'login.html', {"form":form})



def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('login')

@login_required
def profile(request):
    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')
    else:
        user_update_form = UserUpdateForm(instance=request.user)
        profile_update_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_update_form': user_update_form,
        'profile_update_form': profile_update_form
    }

    return render(request, 'profile.html', context)