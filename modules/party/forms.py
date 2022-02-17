from django import forms
from django.forms.widgets import PasswordInput
from modules.common.id_choicefield import IdentificationField


class PartyForm(forms.Form):

    error_messages = {
        'password_mismatch': (
            'The confirmation was different from that you chose.'
        ),
    }

    party_name = forms.CharField(label="Name of the contesting party")

    cname = forms.CharField(label="Candidate's Name")

    age = forms.IntegerField(min_value=0, label="Candidate's Age")

    citype = IdentificationField(label="Identity Proof of the Candidate")

    cidno = forms.CharField(label="Passport / ID Number")

    party_manifesto = forms.CharField(
        widget=forms.Textarea,
        required=False
    )

    party_symbol = forms.ImageField(
        required=False,
        help_text="The maximum size permitted is 2.5 MB"
    )

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

    show_profile = forms.ChoiceField(
        choices=[
            (True, "Show Profile to public"),
            (False, "Hide profile from public")
        ],
        help_text="The Election Commission can override this setting."
    )


class PartyEditForm(forms.Form):

    party_name = forms.CharField()

    cpass = forms.CharField(
        widget=PasswordInput,
        label="Enter your password",
        strip=False,
    )
