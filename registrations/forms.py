from django import forms
from .models import Race, Runner, Registration

class RegistrationForm(forms.Form):
    race = forms.ModelChoiceField(queryset=Race.objects.all(), empty_label="Select a race")
    first_name = forms.CharField(max_length=60)
    last_name = forms.CharField(max_length=60)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20, required=False)
    age = forms.IntegerField(required=False, min_value=5, max_value=120)
    gender = forms.ChoiceField(choices=[('','---')]+list(Runner._meta.get_field('gender').choices), required=False)
    tshirt_size = forms.ChoiceField(choices=Registration._meta.get_field('tshirt_size').choices)

    def clean(self):
        cleaned = super().clean()
        # Further custom validation can be added here
        return cleaned
