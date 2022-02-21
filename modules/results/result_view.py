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


def pretty_percent_divide(dividend, divisor):
    quotient = 0
    if (divisor != 0):
        quotient = round(100 * dividend / divisor, 2)
    return quotient


def voter_turnout_gender(request):
    turnout = mongo_client.db_get_collection("turnout")
    stats = turnout.find_one({"_id": "gender_composition"})
    turnout_total = turnout.find_one({"_id": "gender_all"})
    if stats["Total"] == 0:
        stats_percentage = {
            "Male": 0,
            "Female": 0,
            "Other": 0,
            "Total": 0
        }
    else:
        stats_percentage = {
            "Male": pretty_percent_divide(stats["Male"], stats["Total"]),
            "Female": pretty_percent_divide(stats["Female"], stats["Total"]),
            "Other": pretty_percent_divide(stats["Other"], stats["Total"]),
            "Total": pretty_percent_divide(stats["Total"], stats["Total"]),
        }
    if turnout_total["Total"] == 0:
        stats_turnout = {
            "Male": 0,
            "Female": 0,
            "Other": 0,
            "Total": 0
        }
    else:
        stats_turnout = {
            "Male": pretty_percent_divide(
                stats["Male"],
                turnout_total["Male"]
            ),
            "Female": pretty_percent_divide(
                stats["Female"],
                turnout_total["Female"]
            ),
            "Other": pretty_percent_divide(
                stats["Other"],
                turnout_total["Other"]
            ),
            "Total": pretty_percent_divide(
                stats["Total"],
                turnout_total["Total"]
            ),
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
