from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('deposit/', views.deposit_view, name='deposit'),
    path('transfer/', views.transfer_view, name='transfer'),
    path('transfer/<int:transfer_id>/receipt/', views.transfer_receipt_view, name='transfer_receipt'),
    path('history/', views.transaction_history_view, name='history'),
]
