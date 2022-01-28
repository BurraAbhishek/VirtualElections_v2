from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.hashers import make_password, check_password
from modules.party.forms import PartyForm, PartyEditForm
from bin.mongodb import mongo_client
from modules.common.voteridgen import gen_id


def serve(request) -> render:
    return render(
        request,
        "site_navigation/contestant.html"
    )


def gen_voterID(size):
    voter_id = gen_id(size)
    voters = mongo_client.db_get_collection("user4")
    criterion = dict(_id=voter_id)
    if (voters.find_one(criterion)) is None:
        return voter_id
    else:
        return gen_voterID(size)


def party_view(request):
    authorizationcollection = mongo_client.db_get_collection("mod2")
    authorization = authorizationcollection.find_one(
        {"_id": "access_control"}
    )
    if not authorization["canContestantsRegister"]:
        raise PermissionDenied
    if request.method == "POST":
        form = PartyForm(request.POST, request.FILES)
        if form.is_valid():
            party_name = form.cleaned_data["party_name"]
            if (party_name.lower() == "none of the above"):
                raise PermissionDenied
            if form.cleaned_data["cpd1"] == form.cleaned_data["cpd2"]:
                voter_idtype = form.cleaned_data["citype"]
                voter_id_value = form.cleaned_data["cidno"]
                if form.cleaned_data["show_profile"] == "False":
                    showProfile = False
                else:
                    showProfile = True
                voter = {
                    "_id": gen_voterID(8),
                    "party_name": form.cleaned_data["party_name"],
                    "candidate_name": form.cleaned_data["cname"],
                    "candidate_age": form.cleaned_data["age"],
                    "candidate_identification": {
                        voter_idtype: voter_id_value
                    },
                    "manifesto": form.cleaned_data["party_manifesto"],
                    "password": make_password(form.cleaned_data["cpd1"]),
                    "showProfile": showProfile,
                    "isSymbolUploaded": False,
                    "tosViolation": False
                }
                try:
                    mongo_client.db_insert_one("user3", voter)
                    success_message = " ".join([
                        "You were successfully registered",
                        "as a contestant on this site."
                    ])
                    return render(
                        request,
                        "oops/security_closepage.html",
                        {
                            "success_text": "Registration successful",
                            "success_message": (
                                success_message
                            )
                        }
                    )
                except:
                    raise PermissionDenied
            else:
                return render(
                    request,
                    "oops/password_error.html"
                )
        else:
            raise PermissionDenied
    else:
        return render(
            request,
            "party/registration.html",
            {
                "form": PartyForm()
            }
        )


def update_if_changed(form, id, attr, key, value="", isDefaultValue=True):
    if attr in form.changed_data:
        candidates = mongo_client.db_get_collection("user3")
        if isDefaultValue:
            candidates.find_one_and_update(
                {
                    "_id": id
                },
                {
                    '$set': {
                        key: form.cleaned_data[attr]
                    }
                }
            )
        else:
            candidates.find_one_and_update(
                {
                    "_id": id
                },
                {
                    '$set': {
                        key: value
                    }
                }
            )


def voter_edit_login(request):
    if request.method == "POST":
        auth = PartyEditForm(request.POST)
        if auth.is_valid():
            creds = mongo_client.db_get_collection("user3")
            party_name = auth.cleaned_data["party_name"]
            cred_id = creds.find_one({"party_name": party_name})
            cred_pass = cred_id["password"]
            u_pass = auth.cleaned_data["cpass"]
            if check_password(u_pass, cred_pass):
                cred_idtype = list(
                    cred_id["candidate_identification"].keys()
                )[0]
                form_initial_data = {
                    "party_name": cred_id["party_name"],
                    "cname": cred_id["candidate_name"],
                    "age": cred_id["candidate_age"],
                    "citype": cred_idtype,
                    "cidno": cred_id["candidate_identification"][cred_idtype],
                    "cpd1": u_pass,
                    "cpd2": u_pass,
                }
                if cred_id["_id"] == "00000000":
                    raise PermissionDenied
                request.session["party"] = cred_id["_id"]
                form = PartyForm(
                    initial=form_initial_data
                )
                return render(
                    request,
                    "party/edit.html",
                    {
                        "form": form,
                        "submitlabel": "Save Changes"
                    }
                )
            else:
                return render(
                    request,
                    "party/editlogin.html",
                    {
                        "form": PartyEditForm(),
                        "submitlabel": "Log In"
                    }
                )
        else:
            raise PermissionDenied
    else:
        return render(
            request,
            "party/editlogin.html",
            {
                "form": PartyEditForm(),
                "submitlabel": "Log In"
            }
        )


def voter_edit(request):
    if request.method == "POST":
        auth = PartyForm(request.POST)
        if auth.is_valid():
            try:
                cred_id = str(request.session["party"])
            except:
                raise PermissionDenied
            if auth.cleaned_data["cpd1"] != auth.cleaned_data["cpd2"]:
                return render(
                    request,
                    "oops/password_error.html"
                )
            try:
                update_if_changed(auth, cred_id, "party_name", "party_name")
                update_if_changed(auth, cred_id, "cname", "candidate_name")
                update_if_changed(auth, cred_id, "age", "candidate_age")
                identification = {
                    auth.cleaned_data["citype"]: auth.cleaned_data["cidno"]
                }
                update_if_changed(
                    auth,
                    cred_id,
                    "cidno",
                    "identification",
                    value=identification,
                    isDefaultValue=False
                )
                update_if_changed(
                    auth,
                    cred_id,
                    "cpd1",
                    "password",
                    value=make_password(auth.cleaned_data["cpd1"]),
                    isDefaultValue=False
                )
                if auth.cleaned_data["show_profile"] == "False":
                    showProfile = False
                else:
                    showProfile = True
                update_if_changed(
                    auth,
                    cred_id,
                    "show_profile",
                    "showProfile",
                    value=showProfile,
                    isDefaultValue=False
                )
                if request.session.get("party"):
                    request.session.__delitem__("party")
                return render(
                    request,
                    "oops/security_closepage.html",
                    {
                        "success_text": "Save successful",
                        "success_message": (
                            "Your changes were successfully saved."
                        )
                    }
                )
            except:
                raise PermissionDenied
        else:
            raise PermissionDenied
    else:
        return HttpResponseRedirect("/party/edit/login")
