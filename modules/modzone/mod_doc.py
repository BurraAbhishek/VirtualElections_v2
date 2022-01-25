from django.shortcuts import render
from django.core.exceptions import PermissionDenied


def show_moderator_helppages(request):
    if not request.session.get("mod"):
        raise PermissionDenied
    return render(
        request,
        "modzone/help.html"
    )
