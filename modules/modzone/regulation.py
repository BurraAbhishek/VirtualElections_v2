from django.shortcuts import render
from django.core.exceptions import PermissionDenied


def mod_control_election(request):
    if not request.session.get("mod"):
        raise PermissionDenied
    return render(
        request,
        "modzone/regulation.html"
    )
