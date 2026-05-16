from django import forms
from doctors.models import Appointment

class AppointmentForm(forms.ModelForm):
    
    class Meta:
        model = Appointment
        fields = ['date', 'time_slot',]

        widgets = {
                'date': forms.DateInput(
                    attrs={'type': 'date'}
                )
            }