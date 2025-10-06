"""
RF Analyzer Forms
"""

from django import forms
from .models import MeasurementSession, MeasurementFile


class CsvUploadForm(forms.Form):
    """
    CSV file upload form
    """
    session_name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 2025-01 Measurement'
        }),
        label='Session Name'
    )

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Optional description...'
        }),
        label='Description'
    )

    csv_file = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.csv'
        }),
        label='CSV File',
        help_text='Upload consolidated CSV file (e.g., Bellagio_POC_Rx.csv)'
    )

    def clean_csv_file(self):
        """Validate CSV file"""
        file = self.cleaned_data.get('csv_file')

        if file:
            # Check file extension
            if not file.name.endswith('.csv'):
                raise forms.ValidationError('Only CSV files are allowed.')

            # Check file size (max 200MB)
            if file.size > 200 * 1024 * 1024:
                raise forms.ValidationError('File size must be less than 200MB.')

        return file
