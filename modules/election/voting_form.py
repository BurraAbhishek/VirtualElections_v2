from django import forms


class CastVote(forms.Form):
    party_id = forms.CharField()
