from django import forms
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from bin.mongodb import mongo_client
from modules.common.shrug import is_shrug


class SearchProfile(forms.Form):
    party_name = forms.CharField()


class Disqualify(forms.Form):
    party_id = forms.CharField()
    current_Status = forms.ChoiceField(
        choices=[
            (False, "Clean"),
            (True, "Disqualified")
        ]
    )


def render_modzone(request):
    if not request.session.get("mod"):
        raise PermissionDenied
    if request.method == "POST":
        search_Term = SearchProfile(request.POST)
        if search_Term.is_valid():
            searchTerm = search_Term.cleaned_data["party_name"]
            user3 = mongo_client.db_get_collection("user3")
            searchuser = list(user3.find({"party_name": searchTerm}))
            if len(searchuser) > 1:
                form = []
                for i in searchuser:
                    form.append(
                        Disqualify(
                            initial={
                                "party_id": i["_id"],
                                "current_Status": i["tosViolation"]
                            }
                        )
                    )
                return render(
                    request,
                    "modzone/ban.html",
                    {
                        "search": SearchProfile(),
                        "form": form
                    }
                )
            elif len(searchuser) == 1:
                return render(
                    request,
                    "modzone/ban.html",
                    {
                        "search": SearchProfile(),
                        "form": [Disqualify(
                            initial={
                                "party_id": searchuser[0]["_id"],
                                "current_Status": searchuser[0]["tosViolation"]
                            }
                        )]
                    }
                )
            else:
                return render(
                    request,
                    "modzone/ban.html",
                    {
                        "search": SearchProfile(),
                        "form": None
                    }
                )
        else:
            return render(
                request,
                "modzone/ban.html",
                {
                    "search": SearchProfile(),
                    "form": None
                }
            )
    else:
        return render(
            request,
            "modzone/ban.html",
            {
                "search": SearchProfile(),
                "form": None
            }
        )


def ban(request):
    if not request.session.get("mod"):
        raise PermissionDenied
    if request.method == "POST":
        form = Disqualify(request.POST)
        if form.is_valid():
            uid = form.cleaned_data["party_id"]
            if is_shrug(uid):
                user3 = mongo_client.db_get_collection("user3")
                print(form.cleaned_data["current_Status"])
                if form.cleaned_data["current_Status"] == "False":
                    tosViolation = False
                    user3.find_one_and_update(
                        {"_id": uid},
                        {
                            "$set":
                            {
                                "tosViolation": False
                            }
                        }
                    )
                else:
                    tosViolation = True
                    user3.find_one_and_update(
                        {"_id": uid},
                        {
                            "$set":
                            {
                                "tosViolation": True
                            }
                        }
                    )
            return render(
                request,
                "modzone/ban.html",
                {
                    "search": SearchProfile(),
                    "form": [Disqualify(
                        initial={
                            "party_id": uid,
                            "current_Status": tosViolation
                        }
                    )]
                }
            )
        else:
            return render(
                request,
                "modzone/ban.html",
                {
                    "search": SearchProfile(),
                    "form": [Disqualify()]
                }
            )
    else:
        raise PermissionDenied
