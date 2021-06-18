from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES = {
    ('S','Stripe'),
    ('P','Paypal')
}

class CheckoutForm(forms.Form):
     street_address= forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'16-Nayabazaar'
     }))
     appartment_address=forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder':'Block no 123'
        }))
     country=CountryField(blank_label='(select country)').formfield()
     zip = forms.CharField(widget=forms.TextInput())
     same_billing_address=forms.BooleanField(widget=forms.CheckboxInput())
     save_info = forms.BooleanField(widget=forms.CheckboxInput())
     payment_option=forms.ChoiceField(
        widget=forms.RadioSelect(), choices=PAYMENT_CHOICES)
