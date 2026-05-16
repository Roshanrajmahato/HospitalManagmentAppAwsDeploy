from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from labreports.models import LabTecnicians
from labreports.models import LabTests
from django.db import models


# Rahul Sir Way
class LabTechniciansForm(UserCreationForm):
    emp_id=forms.CharField(max_length=20)
    qualification=forms.CharField(max_length=100)
    year_of_experience=forms.IntegerField()
    address=forms.CharField(max_length=100)
    class Meta:
        model = User
        # fields = "__all__"
        fields = ['username','email','password1','password2']

    

# ChatGpt Way
# class UserForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     class Meta:
#         model = User
#         # fields = "__all__"
#         fields = ['username','email','password']

# class LabTechniciansForm(forms.ModelForm):
#     class Meta:
#         model = LabTecnicians
#         fields = [
#             'emp_id',
#             'qualification',
#             'year_of_experience',
#             'address'
#         ]

class LabTestsForm(forms.ModelForm):

    lab_test = forms.ChoiceField(
        choices=[]
    )
 
    class Meta:

        model = LabTests

        fields = [
            'lab_test',
            'reffered_by',
            'patient_name'
        ]