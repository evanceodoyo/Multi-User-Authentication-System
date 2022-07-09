from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import StudentProfile, TeacherProfile
from django.contrib.auth import get_user_model
User = get_user_model()


"""Create a user registration form."""
class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

"""Create a user update form."""
class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

"""Create a profile update form for students."""

class StudentProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['address', 'avatar']

"""Create a profile update form for teachers."""
class TeacherProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = ['bio', 'address', 'avatar']




