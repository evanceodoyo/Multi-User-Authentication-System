from django.shortcuts import redirect, render
from .forms import UserRegistrationForm, UserUpdateForm, StudentProfileUpdateForm, TeacherProfileUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout

from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user


def home(request):
    return render(request, 'index.html')

@unauthenticated_user
def student_sign_up_view(request):
    context = {}
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_student = True
            user.save()
            user.refresh_from_db()
            user.teacherprofile.first_name = form.cleaned_data['first_name']
            user.teacherprofile.last_name = form.cleaned_data['last_name']
            user.teacherprofile.email = form.cleaned_data['email']
            user.save()
            password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    context['form'] = form

    return render(request, 'student_sign_up.html', context)

@unauthenticated_user
def teacher_sign_up_view(request):
    context = {}
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_teacher = True
            user.save()
            user.refresh_from_db()
            user.teacherprofile.first_name = form.cleaned_data['first_name']
            user.teacherprofile.last_name = form.cleaned_data['last_name']
            user.teacherprofile.email = form.cleaned_data['email']
            user.save()
            password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    context['form'] = form
    
    return render(request, 'teacher_sign_up.html', context)

@unauthenticated_user
def login_view(request):
    context = {}
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Inavlid username or password. Try again!')
    else:
        form  = AuthenticationForm()

    context['form'] = form 

    return render(request,'login.html', context)



def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')
@login_required
def student_profile_view(request):
    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_update_form = StudentProfileUpdateForm(request.POST, request.FILES, instance=request.user.studentprofile)

        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('student_profile')
    else:
        user_update_form = UserUpdateForm(instance=request.user)
        profile_update_form = StudentProfileUpdateForm(instance=request.user.studentprofile)

    context = {
        'user_update_form': user_update_form,
        'profile_update_form': profile_update_form
    }

    return render(request, 'student_profile.html', context)


@login_required
def teacher_profile_view(request):
    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_update_form = TeacherProfileUpdateForm(request.POST, request.FILES, instance=request.user.teacherprofile)

        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('teacher_profile')
    else:
        user_update_form = UserUpdateForm(instance=request.user)
        profile_update_form = TeacherProfileUpdateForm(instance=request.user.teacherprofile)

    context = {
        'user_update_form': user_update_form,
        'profile_update_form': profile_update_form
    }

    return render(request, 'teacher_profile.html', context)