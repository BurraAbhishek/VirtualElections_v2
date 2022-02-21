from django.shortcuts import render
from modules.appeal.tree import appeal_menu
from modules.common.shrug import is_shrug
from bin.mongodb.mongo_client import db_get_collection


def check_appeal(request, mark: dict) -> render:
    return render(
        request,
        "appeal/file.html",
        {
            "mark": mark
        }
    )


def user3_marks(user: str) -> str:
    user3 = db_get_collection("user3")
    suspect = user3.find_one({"_id": user})
    if suspect["tosViolation"]:
        return "cheatMenu"
    else:
        return "cleanMenu"


def select_appeal(request) -> str:
    if request.session.get("mod"):
        return "cleanMenu"
    elif request.session.get("unauthorized"):
        return "illegalAccessMenu"
    elif request.session.get("party"):
        party = request.session["party"]
        if is_shrug(party):
            return user3_marks(party)
        else:
            return "illegalAccessMenu"
    else:
        return "cleanMenu"


def status(request) -> render:
    result = select_appeal(request)
    return check_appeal(request, appeal_menu[result])
