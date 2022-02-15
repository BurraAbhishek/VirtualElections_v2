from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.contrib.auth.hashers import check_password
from modules.voter.forms import VoterEditForm
from modules.election.voting_form import CastVote
from bin.mongodb import mongo_client
from modules.common import crypt, age
from modules.common.age_filter import user_age_filter
from modules.election.filters import user3_filter
from modules.election.filters import age_filter
from modules.election.filters import must_vote_filter


def page_screening(request) -> render:
    return render(
        request,
        "election/editlogin.html",
        {
            "form": VoterEditForm(),
            "submitlabel": "Log In"
        }
    )


def page_voting(request) -> render:
    selected_age = user3_filter()
    selected_provisional = age_filter(selected_age)
    selected = must_vote_filter(selected_provisional)
    selected.reverse()
    for i in selected:
        i["id"] = i["_id"]
    return render(
        request,
        "election/castvote.html",
        {
            "form": CastVote,
            "candidates": selected,
            "submitlabel": "Save Changes"
        }
    )


def duplicate_vote_disallowed(request) -> render:
    return render(
        request,
        "oops/already_voted.html",
        status=403
    )


def voter_screening(request):
    authorizationcollection = mongo_client.db_get_collection("mod2")
    authorization = authorizationcollection.find_one(
        {"_id": "access_control"}
    )
    if not authorization["canVote"]:
        raise PermissionDenied
    if request.method == "POST":
        auth = VoterEditForm(request.POST)
        if auth.is_valid():
            creds = mongo_client.db_get_collection("user4")
            voter_idtype = auth.cleaned_data["citype"]
            voter_id_value = auth.cleaned_data["cidno"]
            cred_id = creds.find_one({
                "identification": {
                    voter_idtype: voter_id_value
                }
            })
            try:
                cred_pass = cred_id["password"]
            except:
                return HttpResponseRedirect("/voter/registration/")
            u_pass = auth.cleaned_data["cpass"]
            if check_password(u_pass, cred_pass):
                voterages = authorizationcollection.find_one(
                    {"_id": "voter_ages"}
                )
                voter_age = age.calculateAge(
                    cred_id["date_of_birth"][0],
                    cred_id["date_of_birth"][1],
                    cred_id["date_of_birth"][2]
                )
                if not user_age_filter(voter_age, voterages):
                    raise PermissionDenied
                voterid = crypt.str_encrypt(cred_id["_id"])
                votes = mongo_client.db_get_collection("vote5")
                vote = list(votes.find({"_id": voterid}))
                if len(vote) > 0:
                    return duplicate_vote_disallowed(request)
                request.session["voter"] = cred_id["_id"]
                return page_voting(request)
            else:
                return page_screening(request)
        else:
            raise PermissionDenied
    else:
        return page_screening(request)
