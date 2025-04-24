from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"), 
    path("login/", views.login_view, name="login"),
    path('reset-password/', views.password_reset_view, name='reset_password'),
    path('account-details/', views.account_details_view, name='account_details'),
]