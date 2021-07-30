from django.urls import path
from .views import (register,
                    login_form,
                    logout_form,
                    profile,
                    show_profile)

app_name='accounts'
urlpatterns = [
    path('register/',register,name='register'),
    path('login/',login_form,name="login"),
    path('logout/',logout_form,name='logout'),
    path('profile/<int:id>',profile,name='profile'),
    path('show_profile/',show_profile,name='show_profile'),
]
