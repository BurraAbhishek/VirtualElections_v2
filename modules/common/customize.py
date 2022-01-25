from django.shortcuts import render


def personalization(request) -> render:
    return render(
        request,
        "customization/customization.html"
    )
