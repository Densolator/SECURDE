import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 2 weeks.")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        
        # Check if a date is not in the past. 
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check if a date is in the allowed range (+2 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=2):
            raise ValidationError(_('Invalid date - renewal more than 2 weeks ahead'))

        # Remember to always return the cleaned data.
        return data

class BorrowBookForm(forms.Form):
    borrow_date = forms.DateField(help_text="Enter a date between now and 2 weeks.")

    def clean_renewal_date(self):
        data = self.cleaned_data['borrow_date']
        
        # Check if a date is not in the past. 
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - date specified is in the past'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=2):
            raise ValidationError(_('Invalid date - you cannot borrow more for more than 2 weeks'))

        # Remember to always return the cleaned data.
        return data