from django.urls import path
from doctors import views

app_name = 'doctors'
urlpatterns = [
    path('', views.alldoctors, name='alldoctors'),
    path('alltreatments/', views.all_treatments, name='alltreatments'),
    path('treatment/<int:treatment_id>/', views.doctors_by_treatments, name='treatment_doctors'),
    path('appointment/<int:doctor_id>/<int:treatment_id>/', views.book_appointment, name='appointment'), 
]