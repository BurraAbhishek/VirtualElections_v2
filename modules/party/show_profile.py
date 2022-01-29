from django.shortcuts import render
from django.http import Http404
from django.core.exceptions import PermissionDenied
from bin.mongodb import mongo_client
from modules.common.shrug import is_shrug


def can_view(request, profile, setting) -> bool:
    if request.session.get("mod"):
        return True
    elif setting["views"] == "Show All":
        return True
    elif setting["views"] == "Hide All":
        return False
    else:
        return bool(profile["showProfile"])


def canShowMark(request, profile, setting) -> bool:
    if request.session.get("party"):
        if str(request.session["party"]) == str(profile["_id"]):
            return False
    if not profile["tosViolation"]:
        return False
    elif request.session.get("mod"):
        return True
    else:
        return setting["showTosViolation"]


def show_contestant(request, id):
    id_cleaned = str(id)
    if is_shrug(id_cleaned):
        if id_cleaned == "00000000" and not request.session.get("mod"):
            raise PermissionDenied
        contestants = mongo_client.db_get_collection("user3")
        contestant = contestants.find_one({"_id": id_cleaned})
        if contestant is None:
            raise Http404
        mod2 = mongo_client.db_get_collection("mod2")
        profile_setting = mod2.find_one({"_id": "candidate_privacy"})
        if not can_view(request, contestant, profile_setting):
            raise PermissionDenied
        can_mark = canShowMark(request, contestant, profile_setting)
        return render(
            request,
            "party/profile.html",
            {
                "party": contestant,
                "canShowTOSViolation": can_mark,
            }
        )
    else:
        raise PermissionDenied
