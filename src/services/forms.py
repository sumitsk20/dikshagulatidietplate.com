from django import forms
from django.core.exceptions import ValidationError
# from captcha.fields import ReCaptchaField
from .models import Appointment, Subscriber

class AppointmentForm(forms.ModelForm):
   # captcha = ReCaptchaField()
    class Meta:
        model = Appointment
        fields = ['name','email','number','service','message']

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields['service'].empty_label = '--Select your concern--'

    def clean_number(self):
        print self.cleaned_data
        client_phone = self.cleaned_data['number']
        if client_phone.isdigit() and not client_phone.isalpha():
            min_length = 10
            max_length = 12
            ph_length = str(client_phone)
            if len(ph_length) < min_length or len(ph_length) > max_length:
                raise ValidationError('Phone number length not valid')
        else:
            raise ValidationError('Please enter a valid phone number')
        return client_phone

