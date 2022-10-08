from django.urls import path
from .views import home, login_view, logout_view, profile, sign_up

urlpatterns = [
    path('', home, name='home'),
    path('sign-up/', sign_up, name='sign_up'),
    path('login/', login_view, name="login" ),
    path('profile/', profile, name='profile'),
    path('logout/', logout_view, name="logout" ),
]