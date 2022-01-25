from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.contrib.auth.hashers import check_password
from bin.mongodb import mongo_client
from modules.modzone.forms import ModLogin


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
                    return render(
                        request,
                        "oops/corrections_fakemod.html",
                    )
            except:
                return render(
                    request,
                    "oops/corrections_fakemod.html",
                )
        else:
            return render(
                request,
                "oops/corrections_fakemod.html",
            )
    else:
        if request.session.get("mod"):
            return render(
                request,
                "modzone/mainmenu.html",
            )
        else:
            raise PermissionDenied
