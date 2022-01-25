from django.shortcuts import render
from modules.modzone.electorsform import AccessMod
from bin.mongodb import mongo_client


def strtobool(value: str) -> bool:
    if value == "True":
        return True
    elif value == "False":
        return False


def update_controls(form, key, value):
    mod2 = mongo_client.db_get_collection("mod2")
    if key in form.changed_data:
        mod2.find_one_and_update(
            {
                "_id": "access_control"
            },
            {
                '$set': {
                    key: strtobool(value)
                }
            }
        )


def render_access(request) -> render:
    mod2 = mongo_client.db_get_collection("mod2")
    accessControls = mod2.find_one({"_id": "access_control"})
    accessForm = {
        "canVotersRegister": accessControls["canVotersRegister"],
        "canContestantsRegister": accessControls["canContestantsRegister"],
        "canVote": accessControls["canVote"],
        "canShowResults": accessControls["canShowResults"]
    }
    return render(
        request,
        "modzone/accesscontrols.html",
        {
            "form": AccessMod(initial=accessForm)
        }
    )


def control_access(request):
    if request.method == "POST":
        form = AccessMod(request.POST)
        if form.is_valid():
            update_controls(
                form,
                "canVotersRegister",
                form.cleaned_data["canVotersRegister"]
            )
            update_controls(
                form,
                "canContestantsRegister",
                form.cleaned_data["canContestantsRegister"]
            )
            update_controls(
                form,
                "canVote",
                form.cleaned_data["canVote"]
            )
            update_controls(
                form,
                "canShowResults",
                form.cleaned_data["canShowResults"]
            )
        return render_access(request)
    else:
        return render_access(request)
