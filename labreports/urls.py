from django.urls import path
from labreports import views

    
urlpatterns = [
    path('register_lab_technician/', views.register_lab_technician, name='register_lab_technician'),
    path('labtech_home/',views.labtech_home,name='labtech_home'),
    path('all-lab-tests/',views.all_lab_tests,name='all_lab_tests'),
    path('dashboard/',views.lab_dashboard,name='lab_dashboard'),
    path('add_test/',views.add_test, name='add_test'),
    path('edit_test/<int:id>/', views.edit_test, name='edit_test'),
    # path('all_lab_tests/<int:doctor_id>/',views.add_lab_test,name='all_lab_tests'), # From Doctor
]

