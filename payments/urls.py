from django.urls import path
from payments import views


urlpatterns = [

    path('create-discharge/',views.create_discharge,name='create-discharge'),
    path('bill/<int:pk>/',views.discharge_bill,name='discharge_bill'),
    path('create-order/<int:pk>/', views.create_payment_order, name='create_payment_order'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('bill-list/',views.discharge_list,name='discharge_list'),

]