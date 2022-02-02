from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from bin.mongodb import mongo_client
from modules.results import result_resolver
from modules.common.shrug import is_shrug


def reset_result(request):
    if not request.session.get("mod"):
        raise PermissionDenied
    result_resolver.gender_turnout()
    result_resolver.recompute_result()
    return HttpResponseRedirect("/modzone/authenticate")


def voter_turnout_gender(request):
    turnout = mongo_client.db_get_collection("turnout")
    stats = turnout.find_one({"_id": "gender_composition"})
    turnout_total = turnout.find_one({"_id": "gender_all"})
    if stats["Total"] == 0:
        stats_percentage = {
            "Male": 0,
            "Female": 0,
            "Other": 0
        }
    else:
        stats_percentage = {
            "Male": round(stats["Male"] / stats["Total"], 2),
            "Female": round(stats["Female"] / stats["Total"], 2),
            "Other": round(stats["Other"] / stats["Total"], 2),
        }
    if turnout_total["Total"] == 0:
        stats_turnout = {
            "Male": 0,
            "Female": 0,
            "Other": 0
        }
    else:
        stats_turnout = {
            "Male": round(stats["Male"] / turnout_total["Male"], 2),
            "Female": round(stats["Female"] / turnout_total["Female"], 2),
            "Other": round(stats["Other"] / turnout_total["Other"], 2),
            "Total": round(stats["Total"] / turnout_total["Total"], 2)
        }
    return render(
        request,
        "results/turnout_gender.html",
        {
            "total": turnout_total,
            "stats": stats,
            "stats_percent": stats_percentage,
            "turnout": stats_turnout
        }
    )


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
