from django import forms


class ModLogin(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput, strip=False)
