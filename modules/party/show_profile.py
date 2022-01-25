from django.shortcuts import render
from django.http import Http404
from django.core.exceptions import PermissionDenied
from bin.mongodb import mongo_client
from modules.common.shrug import is_shrug


def show_contestant(request, id):
    id_cleaned = str(id)
    if is_shrug(id_cleaned):
        if id_cleaned == "00000000" and not request.session.get("mod"):
            raise PermissionDenied
        contestants = mongo_client.db_get_collection("user3")
        contestant = contestants.find_one({"_id": id_cleaned})
        if contestant is None:
            raise Http404
        return render(
            request,
            "party/profile.html",
            {"party": contestant}
        )
    else:
        raise PermissionDenied
