from django import forms
from payments.models import DischargeSummary


class DischargeSummaryForm(forms.ModelForm):

    class Meta:

        model = DischargeSummary

        exclude = [

            'total_days',
            'bed_total',
            'nursing_total',
            'doctor_total',
            'misc_total',
            'room_total',
            'food_total',
            'medicine_total',
            'grand_total'

        ]

        widgets = {

        'doa': forms.DateInput(
            attrs={'type': 'date'}
        ),

        'dod': forms.DateInput(
            attrs={'type': 'date'}
        ),

        'description': forms.Textarea(
            attrs={'rows': 3}
        ),

        }