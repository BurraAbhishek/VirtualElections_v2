from django import forms
from django.forms.widgets import PasswordInput
from modules.common.id_choicefield import IdentificationField


class VoterForm(forms.Form):

    error_messages = {
        'password_mismatch': (
            'The confirmation was different from that you chose.'
        ),
    }

    cname = forms.CharField(label="Voter's Name")

    cdob = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date"
                }
            ),
        label="Date of Birth"
    )

    cgender = forms.ChoiceField(
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other')
        ],
        label="Gender"
    )

    citype = IdentificationField(label="Identification Proof")

    cidno = forms.CharField(label="Passport / ID Number")

    cpd1 = forms.CharField(
        widget=PasswordInput,
        label="Enter your password",
        strip=False,
    )

    cpd2 = forms.CharField(
        widget=PasswordInput,
        label="Confirm Password",
        strip=False,
        help_text=("Enter the same password as before, for verification")
    )


class VoterEditForm(forms.Form):
    citype = IdentificationField(label="Identification Proof")

    cidno = forms.CharField(label="Passport / ID Number")

    cpass = forms.CharField(
        widget=PasswordInput,
        label="Enter your password",
        strip=False,
    )
