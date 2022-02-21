from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.contrib.auth.hashers import check_password
from bin.mongodb import mongo_client
from modules.modzone.forms import ModLogin
from modules.common.shrug import is_shrug


def log_violation(request) -> render:
    if request.session.get("party"):
        user3 = mongo_client.db_get_collection("user3")
        suspect = request.session["party"]
        if is_shrug(suspect):
            user3.update_one(
                {
                    "_id": suspect
                },
                {
                    "$set": {
                        "tosViolation": True
                    }
                }
            )
    else:
        request.session["unauthorized"] = 1
    return render(
        request,
        "oops/corrections_fakemod.html",
        status=403
    )


def authenticate_mod(request) -> render:
    if request.method == "POST":
        form = ModLogin(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                mods = mongo_client.db_get_collection("mod1")
                loggedInMod = dict(_id=username)
                requested_mod = mods.find_one(loggedInMod)
                mod_hash = requested_mod["password"]
                request.session["mod"] = username
                if check_password(password, mod_hash):
                    return render(
                        request,
                        "modzone/mainmenu.html",
                    )
                else:
                    return log_violation(request)
            except:
                return log_violation(request)
        else:
            return log_violation(request)
    else:
        if request.session.get("mod"):
            return render(
                request,
                "modzone/mainmenu.html",
            )
        else:
            raise PermissionDenied
