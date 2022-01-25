from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from bin.mongodb import mongo_client
from modules.results.result_resolver import resolve_result


def result_view(request):
    authorizationcollection = mongo_client.db_get_collection("mod2")
    authorization = authorizationcollection.find_one(
        {"_id": "access_control"}
    )
    if not authorization["canShowResults"]:
        raise PermissionDenied
    result_list = resolve_result()
    return render(
        request,
        "results/show_result.html",
        {
            "resultlist": result_list
        }
    )
