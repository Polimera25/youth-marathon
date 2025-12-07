from django import forms
from .models import Race, Runner, Registration


class RegistrationForm(forms.Form):
    race = forms.ModelChoiceField(
        queryset=Race.objects.all(),
        empty_label="Select a race",
        label="Race"
    )
    first_name = forms.CharField(
        max_length=60,
        label="First name"
    )
    last_name = forms.CharField(
        max_length=60,
        label="Last name"
    )
    email = forms.EmailField(
        label="Email"
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        label="Phone"
    )
    age = forms.IntegerField(
        required=False,
        min_value=5,
        max_value=120,
        label="Age"
    )
    gender = forms.ChoiceField(
        choices=[('', '---')] + list(Runner._meta.get_field('gender').choices),
        required=False,
        label="Gender"
    )
    tshirt_size = forms.ChoiceField(
        choices=Registration._meta.get_field('tshirt_size').choices,
        label="T-Shirt Size"
    )

    # NEW FIELDS
    emergency_contact_name = forms.CharField(
        max_length=100,
        required=False,
        label="Emergency contact name",
    )
    emergency_contact_phone = forms.CharField(
        max_length=20,
        required=False,
        label="Emergency contact number",
    )

    def clean(self):
        cleaned = super().clean()
        # Place for extra validation later (e.g., age vs race distance)
        return cleaned


class PaymentForm(forms.ModelForm):
    """
    Step 2 form – only collects / updates the UTR number
    for an existing Registration.
    """

    class Meta:
        model = Registration
        fields = ["utr_number"]
        labels = {
            "utr_number": "UTR / Transaction ID",
        }
        widgets = {
            "utr_number": forms.TextInput(
                attrs={
                    "placeholder": "Enter UTR / transaction ID"
                }
            )
        }
