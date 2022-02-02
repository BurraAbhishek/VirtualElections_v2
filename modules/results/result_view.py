from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from bin.mongodb import mongo_client
from modules.results import result_resolver


def reset_result(request):
    if not request.session.get("mod"):
        raise PermissionDenied
    result_resolver.gender_turnout()
    result_resolver.recompute_result()
    return HttpResponseRedirect("/modzone/authenticate")


def result_view(request):
    authorizationcollection = mongo_client.db_get_collection("mod2")
    authorization = authorizationcollection.find_one(
        {"_id": "access_control"}
    )
    if not authorization["canShowResults"]:
        raise PermissionDenied
    result_list = result_resolver.resolve_result()
    return render(
        request,
        "results/show_result.html",
        {
            "resultlist": result_list
        }
    )
