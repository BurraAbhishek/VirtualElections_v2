from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from modules.modzone.electorsform import ElectorMod
from bin.mongodb.mongo_client import db_get_collection


def age_regulation(setting, minAge, maxAge):
    if (minAge <= 0) and (maxAge >= 100):
        return False
    else:
        return setting


def update_if_changed(collection, form, formKey, id, dbKey, value=None):
    if formKey in form.cleaned_data:
        if value is None:
            value = form.cleaned_data[formKey]
        collection.find_one_and_update(
            {"_id": id},
            {
                "$set":
                {
                    dbKey: value
                }
            }
        )


def voter_age_requirement(form) -> bool:
    b1 = form.cleaned_data["votersMustHaveAgeConstraint"]
    i1 = form.cleaned_data["votersMinAge"]
    i2 = form.cleaned_data["votersMaxAge"]
    b2 = (i1 <= 0) and (i2 >= 100)
    return b1 or b2


def candidate_age_requirement(form) -> bool:
    b1 = form.cleaned_data["candidatesMustHaveAgeConstraint"]
    i1 = form.cleaned_data["candidatesMinAge"]
    i2 = form.cleaned_data["candidatesMaxAge"]
    b2 = (i1 <= 0) and (i2 >= 100)
    return b1 or b2


def mod_get_controls(request):
    mod2 = db_get_collection("mod2")
    cprivacy = mod2.find_one({"_id": "candidate_privacy"})
    vage = mod2.find_one({"_id": "voter_ages"})
    cage = mod2.find_one({"_id": "candidate_ages"})
    mustvote = mod2.find_one({"_id": "candidate_must_vote"})
    initialData = {
        "Candidate_Privacy": cprivacy["views"],
        "show_violated_warning": cprivacy["showTosViolation"],
        "mustBeAVoter": mustvote["boolValue"],
        "votersMustHaveAgeConstraint": age_regulation(
            vage["boolRequired"],
            vage["minAge"],
            vage["maxAge"]
        ),
        "candidatesMustHaveAgeConstraint": age_regulation(
            cage["boolRequired"],
            cage["minAge"],
            cage["maxAge"]
        )
    }
    initialData["votersMinAge"] = vage["minAge"]
    initialData["votersMaxAge"] = vage["maxAge"]
    initialData["candidatesMinAge"] = cage["minAge"]
    initialData["candidatesMaxAge"] = cage["maxAge"]
    return render(
            request,
            "modzone/regulation.html",
            {
                "form": ElectorMod(initial=initialData),
                "submitlabel": "Save settings"
            }
        )


def post_mod_control(request):
    form = ElectorMod(request.POST)
    if form.is_valid():
        mod2 = db_get_collection("mod2")
        update_if_changed(
            mod2,
            form,
            "Candidate_Privacy",
            "candidate_privacy",
            "views"
            )
        update_if_changed(
            mod2,
            form,
            "show_violated_warning",
            "candidate_privacy",
            "showTosViolation"
            )
        update_if_changed(
            mod2,
            form,
            "mustBeAVoter",
            "candidate_must_vote",
            "boolValue"
            )
        if not voter_age_requirement(form):
            mod2.find_one_and_update(
                {"_id": "voter_ages"},
                {
                    "$set":
                    {
                        "boolRequired": True,
                        "minAge": form.cleaned_data["votersMinAge"],
                        "maxAge": form.cleaned_data["votersMaxAge"],
                    }
                }
            )
        else:
            mod2.find_one_and_update(
                {"_id": "voter_ages"},
                {
                    "$set":
                    {
                        "boolRequired": False,
                        "minAge": 0,
                        "maxAge": 100,
                    }
                }
            )
        if not candidate_age_requirement(form):
            mod2.find_one_and_update(
                {"_id": "voter_ages"},
                {
                    "$set":
                    {
                        "boolRequired": True,
                        "minAge": form.cleaned_data["candidatesMinAge"],
                        "maxAge": form.cleaned_data["candidatesMaxAge"],
                    }
                }
            )
        else:
            mod2.find_one_and_update(
                {"_id": "candidate_ages"},
                {
                    "$set":
                    {
                        "boolRequired": False,
                        "minAge": 0,
                        "maxAge": 100,
                    }
                }
            )


def mod_control_election(request):
    if not request.session.get("mod"):
        raise PermissionDenied
    if request.method == "POST":
        post_mod_control(request)
        return mod_get_controls(request)
    else:
        return mod_get_controls(request)
