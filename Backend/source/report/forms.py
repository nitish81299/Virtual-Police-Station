from django import forms

from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = [
            'victim',
            'fathers_name',
            'address',
            'email',
            'aadhaar_number',
            'contact',
            'category_of_crime',
            'place_of_crime',
            'date_time_of_crime',
            'description',
            'other_details'
        ]
