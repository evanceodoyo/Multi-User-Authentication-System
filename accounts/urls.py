from django.urls import path
from .views import home, student_sign_up_view, teacher_sign_up_view, login_view, logout_view, student_profile_view, teacher_profile_view

urlpatterns = [
    path('', home, name='home'),
    path('student_sign_up/', student_sign_up_view, name='student_sign_up'),
    path('teacher_sign_up/', teacher_sign_up_view, name='teacher_sign_up'),
    path('login/', login_view, name="login" ),
    path('s_profile/', student_profile_view, name='student_profile'),
    path('t_profile/', teacher_profile_view, name='teacher_profile'),
    path('logout/', logout_view, name="logout" ),
]