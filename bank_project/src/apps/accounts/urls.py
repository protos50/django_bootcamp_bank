from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('deposit/', views.deposit_view, name='deposit'),
    path('transfer/', views.transfer_view, name='transfer'),
    path('transfer/<int:transfer_id>/receipt/', views.transfer_receipt_view, name='transfer_receipt'),
    path('history/', views.transaction_history_view, name='history'),
    path('favorite/<int:user_id>/toggle/', views.toggle_favorite_view, name='toggle_favorite'),
]
