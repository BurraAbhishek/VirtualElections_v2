from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.contrib.auth.hashers import make_password, check_password
from modules.voter.forms import VoterForm, VoterEditForm
from modules.common.voteridgen import gen_id
from bin.mongodb import mongo_client
import datetime


def serve(request) -> render:
    return render(
        request,
        "site_navigation/voter.html"
    )


def gen_voterID(size):
    voter_id = gen_id(size)
    voters = mongo_client.db_get_collection("user4")
    criterion = dict(_id="Test(Test)")
    if (voters.find_one(criterion)) is None:
        return voter_id
    else:
        return gen_voterID(size)


def voter_view(request):
    authorizationcollection = mongo_client.db_get_collection("mod2")
    authorization = authorizationcollection.find_one(
        {"_id": "access_control"}
    )
    if not authorization["canVotersRegister"]:
        raise PermissionDenied
    if request.method == "POST":
        form = VoterForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["cpd1"] == form.cleaned_data["cpd2"]:
                voter_idtype = form.cleaned_data["citype"]
                voter_id_value = form.cleaned_data["cidno"]
                dateobject = form.cleaned_data["cdob"]
                dates = [
                    int(dateobject.strftime("%Y")),
                    int(dateobject.strftime("%m")),
                    int(dateobject.strftime("%d")),
                ]
                voter = {
                    "_id": gen_voterID(12),
                    "name": form.cleaned_data["cname"],
                    "date_of_birth": dates,
                    "gender": form.cleaned_data["cgender"],
                    "identification": {
                        voter_idtype: voter_id_value
                    },
                    "password": make_password(form.cleaned_data["cpd1"]),
                }
                try:
                    mongo_client.db_insert_one("user4", voter)
                    success_message = " ".join([
                        "You were successfully registered",
                        "as a voter on this site."
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
            "voter/registration.html",
            {
                "form": VoterForm()
            }
        )


def update_if_changed(form, id, attr, key, value="", isDefaultValue=True):
    if attr in form.changed_data:
        voters = mongo_client.db_get_collection("user4")
        if isDefaultValue:
            voters.find_one_and_update(
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
            voters.find_one_and_update(
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
        auth = VoterEditForm(request.POST)
        if auth.is_valid():
            creds = mongo_client.db_get_collection("user4")
            voter_idtype = auth.cleaned_data["citype"]
            voter_id_value = auth.cleaned_data["cidno"]
            cred_id = creds.find_one({
                "identification":
                {
                    voter_idtype: voter_id_value
                }
            })
            cred_pass = cred_id["password"]
            u_pass = auth.cleaned_data["cpass"]
            if check_password(u_pass, cred_pass):
                cred_idtype = list(cred_id["identification"].keys())[0]
                cred_dob = datetime.datetime(
                    cred_id["date_of_birth"][0],
                    cred_id["date_of_birth"][1],
                    cred_id["date_of_birth"][2]
                )
                form_initial_data = {
                    "cname": cred_id["name"],
                    "cdob": cred_dob,
                    "cgender": cred_id["gender"],
                    "citype": cred_idtype,
                    "cidno": cred_id["identification"][cred_idtype],
                    "cpd1": u_pass,
                    "cpd2": u_pass
                }
                request.session["voter"] = cred_id["_id"]
                form = VoterForm(
                    initial=form_initial_data
                )
                return render(
                    request,
                    "voter/edit.html",
                    {
                        "form": form,
                        "submitlabel": "Save Changes"
                    }
                )
            else:
                return render(
                    request,
                    "voter/editlogin.html",
                    {
                        "form": VoterEditForm(),
                        "submitlabel": "Log In"
                    }
                )
        else:
            raise PermissionDenied
    else:
        return render(
            request,
            "voter/editlogin.html",
            {
                "form": VoterEditForm(),
                "submitlabel": "Log In"
            }
        )


def voter_edit(request):
    if request.method == "POST":
        auth = VoterForm(request.POST)
        if auth.is_valid():
            try:
                cred_id = str(request.session["voter"])
            except:
                raise PermissionDenied
            try:
                print(auth.changed_data)
                update_if_changed(auth, cred_id, "cname", "name")
                dateobject = auth.cleaned_data["cdob"]
                dates = [
                    int(dateobject.strftime("%Y")),
                    int(dateobject.strftime("%m")),
                    int(dateobject.strftime("%d")),
                ]
                update_if_changed(
                    auth,
                    cred_id,
                    "cdob",
                    "date_of_birth",
                    value=dates,
                    isDefaultValue=False
                )
                update_if_changed(auth, cred_id, "cgender", "gender")
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
        return HttpResponseRedirect("/voter/edit/login")
