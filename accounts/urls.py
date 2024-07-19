from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('import/', views.import_accounts, name='import'),
    path('', views.list_accounts, name='list'),
    path('<uuid:pk>/', views.account_detail, name='detail'),
    path('transfer/', views.transfer_funds, name='transfer'),
]
