from django import forms


class AccessMod(forms.Form):

    canVotersRegister = forms.ChoiceField(
        label="",
        choices=[
            (True, "Open Voter Registrations"),
            (False, "Close Voter Registrations")
        ]
    )

    canContestantsRegister = forms.ChoiceField(
        label="",
        choices=[
            (True, "Open Contestant Registrations"),
            (False, "Close Contestants Registrations")
        ]
    )

    canVote = forms.ChoiceField(
        label="",
        choices=[
            (True, "Open voting session"),
            (False, "Close voting session")
        ]
    )

    canShowResults = forms.ChoiceField(
        label="",
        choices=[
            (True, "Show results to public"),
            (False, "Don't show results")
        ]
    )


class ElectorMod(forms.Form):

    Candidate_Privacy = forms.ChoiceField(
        choices=[
            ('Default', 'Default'),
            ('Show All', 'Show All'),
            ('Hide All', 'Hide All')
        ],
        help_text=(
            "Show or hide candidates profiles. Default: based on preferences."
        )
    )

    show_violated_warning = forms.BooleanField(
        help_text=(
            "When enabled, disqualified candidates will be publicly marked."
        ),
        required=False
    )

    mustBeAVoter = forms.BooleanField(
        help_text=" ".join([
            "Selecting this option requires that",
            "contestants must be registered as voters."
        ]),
        required=False
    )

    votersMustHaveAgeConstraint = forms.BooleanField(
        help_text="Selecting this option enforces age constraints on voters.",
        required=False
    )

    votersMinAge = forms.IntegerField(
        min_value=0,
        max_value=100,
        help_text="The minimum age required to vote, from 0",
        required=False
    )

    votersMaxAge = forms.IntegerField(
        min_value=0,
        max_value=100,
        help_text=(
            "The maximum age required to vote, 100 for no upper age bound"
        ),
        required=False
    )

    candidatesMustHaveAgeConstraint = forms.BooleanField(
        help_text=(
            "Selecting this option enforces age constraints on candidates."
        ),
        required=False
    )

    candidatesMinAge = forms.IntegerField(
        min_value=0,
        max_value=100,
        help_text="The minimum age required to contest for power, from 0",
        required=False
    )

    candidatesMaxAge = forms.IntegerField(
        min_value=0,
        max_value=100,
        help_text=" ".join([
            "The maximum age required to contest for power,",
            "100 for no upper age bound"
        ]),
        required=False
    )
