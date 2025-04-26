from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"), 
    path('logout/', views.logout_view, name='logout'),
    path("login/", views.login_view, name="login"),
    path('verify-email/', views.reset_password_view, name='reset_password'),
    path('account-details/', views.account_details_view, name='account_details'),
    path('user_profile/', views.user_profile, name='user_profile'),
]