from django.urls import path
from . import views

urlpatterns = [
    path('explore/', views.explore_clubs, name='explore'),
    path('swipe/<int:club_id>/<str:action>/', views.swipe_club, name='swipe_club'),
    path('cart/', views.cart_view, name='cart'),
    path('join/<int:club_id>/', views.join_club, name='join_club'),
    path('club/<int:club_id>/', views.club_detail, name='club_detail'),
]
